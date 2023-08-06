from collections import namedtuple
from .utils import get_latest_opset_version
from ebm2onnx import graph
from ebm2onnx import ebm
import ebm2onnx.operators as ops

import numpy as np
import onnx

from interpret.glassbox import ExplainableBoostingClassifier, ExplainableBoostingRegressor


onnx_type_for={
    'float': onnx.TensorProto.FLOAT,
    'double': onnx.TensorProto.DOUBLE,
    'int': onnx.TensorProto.INT64,
    'str': onnx.TensorProto.STRING,
}


def infer_features_dtype(dtype, feature_name):
    feature_dtype = onnx.TensorProto.DOUBLE
    if dtype is not None:
        feature_dtype = onnx_type_for[dtype[feature_name]]

    return feature_dtype

def to_onnx(model, dtype, name=None,
            predict_proba=False,
            explain=False
            ):
    """Converts an EBM model to ONNX

    Args:
        model: The EBM model, trained with interpretml
        dtype: A dict containing the type of each input feature. Types are expressed as strings, the following values are supported: float, double, int, str.
        name: [Optional] The name of the model
        predict_proba: [Optional] For classification models, output prediction probabilities instead of class
        explain: [Optional] Adds an additional output with the score per feature per class

    Returns:
        An ONNX model.
    """
    #target_opset = target_opset or get_latest_opset_version()
    root = graph.create_graph(name=name)

    class_index=0
    inputs = [None for _ in model.feature_names]
    parts = []

    # first compute the score of each feature
    for feature_index in range(len(model.feature_names)):
        feature_name=model.feature_names[feature_index]
        feature_type=model.feature_types[feature_index]
        feature_group=model.feature_groups_[feature_index]

        if feature_type == 'continuous':
            bins = [np.NINF, np.NINF] + list(model.preprocessor_.col_bin_edges_[feature_group[0]])
            additive_terms = model.additive_terms_[feature_index]

            feature_dtype = infer_features_dtype(dtype, feature_name)
            part = graph.create_input(root, feature_name, feature_dtype, [None])
            part = ops.flatten()(part)
            inputs[feature_index] = part
            part = ebm.get_bin_index_on_continuous_value(bins)(part)
            part = ebm.get_bin_score_1d(additive_terms)(part)
            parts.append(part)

        elif feature_type == 'categorical':
            col_mapping = model.preprocessor_.col_mapping_[feature_group[0]]
            additive_terms = model.additive_terms_[feature_index]

            part = graph.create_input(root, feature_name, onnx.TensorProto.STRING, [None])
            part = ops.flatten()(part)
            inputs[feature_index] = part
            part = ebm.get_bin_index_on_categorical_value(col_mapping)(part)
            part = ebm.get_bin_score_1d(additive_terms)(part)
            parts.append(part)

        elif feature_type == 'interaction':
            i_parts = []
            for index in range(2):
                i_feature_index = feature_group[index]
                i_feature_type = model.feature_types[i_feature_index]

                if i_feature_type == 'continuous':
                    bins = [np.NINF, np.NINF] + list(model.pair_preprocessor_.col_bin_edges_[i_feature_index])
                    input = graph.strip_to_transients(inputs[i_feature_index])
                    i_parts.append(ebm.get_bin_index_on_continuous_value(bins)(input))

                elif i_feature_type == 'categorical':
                    col_mapping = model.preprocessor_.col_mapping_[i_feature_index]
                    input = graph.strip_to_transients(inputs[i_feature_index])
                    i_parts.append(ebm.get_bin_index_on_categorical_value(col_mapping)(input))

                else:
                    raise NotImplementedError(f"feature type {feature_type} is not supported in interactions")

            part = graph.merge(*i_parts)
            additive_terms = model.additive_terms_[feature_index]
            part = ebm.get_bin_score_2d(np.array(additive_terms))(part)
            parts.append(part)

        else:
            raise NotImplementedError(f"feature type {feature_type} is not supported")

    # compute scores, predict and proba
    g = graph.merge(*parts)
    if type(model) is ExplainableBoostingClassifier:
        g, scores_output_name = ebm.compute_class_score(model.intercept_)(g)
        if len(model.classes_) == 2: # binary classification
            if predict_proba is False:
                g = ebm.predict_class(binary=True)(g)
                g = graph.add_output(g, g.transients[0].name, onnx.TensorProto.INT64, [None])
            else:
                g = ebm.predict_proba(binary=True)(g)
                g = graph.add_output(g, g.transients[0].name, onnx.TensorProto.FLOAT, [None, len(model.classes_)])
        else:
            if predict_proba is False:
                g = ebm.predict_class(binary=False)(g)
                g = graph.add_output(g, g.transients[0].name, onnx.TensorProto.INT64, [None])
            else:
                g = ebm.predict_proba(binary=False)(g)
                g = graph.add_output(g, g.transients[0].name, onnx.TensorProto.FLOAT, [None, len(model.classes_)])
    elif type(model) is ExplainableBoostingRegressor:
        g, scores_output_name = ebm.compute_class_score(np.array([model.intercept_]))(g)
        g = ebm.predict_value()(g)
        g = graph.add_output(g, g.transients[0].name, onnx.TensorProto.FLOAT, [None])
    else:
        raise NotImplementedError("{} models are not supported".format(type(model)))

    if explain is True:
        if len(model.classes_) == 2:
            g = graph.add_output(g, scores_output_name, onnx.TensorProto.FLOAT, [None, len(model.feature_names)])
        else:
            g = graph.add_output(g, scores_output_name, onnx.TensorProto.FLOAT, [None, len(model.feature_names), len(model.classes_)])

    model = graph.compile(g)
    return model
