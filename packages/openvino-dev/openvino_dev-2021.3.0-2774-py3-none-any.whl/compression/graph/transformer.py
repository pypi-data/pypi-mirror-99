#
# Copyright 2020-2021 Intel Corporation.
#
# This software and the related documents are Intel copyrighted materials,
# and your use of them is governed by the express license under which they
# were provided to you (End User License Agreement for the Intel(R) Software
# Development Products (Version October 2018)). Unless the License provides
# otherwise, you may not use, modify, copy, publish, distribute, disclose or
# transmit this software or the related documents without Intel's prior
# written permission.
#
# This software and the related documents are provided as is, with no
# express or implied warranties, other than those that are expressly
# stated in the License.

from .special_operations import QUANTIZE_AGNOSTIC_OPERATIONS
from .passes import InsertFakeQuantize, FakeQuantizePropagation, FakeQuantizeOptimization, RemoveFakeQuantize, \
    SpecialBlocksMarker
from .utils import find_operation_matches, get_operation_list, preprocess_ignored_params


class GraphTransformer:
    def __init__(self, hardware_config, quantize_inputs=False):
        self.target_device = hardware_config[0]['target_device']
        hw_ops = get_operation_list(hardware_config)

        quantize_agnostic_operations = [op[1] for op in find_operation_matches(
            QUANTIZE_AGNOSTIC_OPERATIONS, hw_ops)]

        quantize_operations = []
        for hw_op in hw_ops:
            if hw_op not in quantize_agnostic_operations:
                quantize_operations.append(hw_op)

        self.nodes_marker = SpecialBlocksMarker()

        self.fq_insertion = InsertFakeQuantize()
        self.fq_insertion.quantize_operations = quantize_operations

        self.fq_propagation = FakeQuantizePropagation()
        self.fq_propagation.quantize_agnostic_operations = quantize_agnostic_operations
        self.fq_propagation.quantize_inputs = quantize_inputs
        self.fq_propagation.quantize_operations = quantize_operations

        self.fq_optimization = FakeQuantizeOptimization()

        self.fq_removal = RemoveFakeQuantize()
        self.fq_removal.quantize_agnostic_operations = quantize_agnostic_operations
        self.fq_removal.quantize_operations = quantize_operations

    def _insert_fake_quantize(self, graph):
        if self.fq_insertion.ignored_params['skip_model']:
            return graph

        self.nodes_marker.mark_ignored_blocks(graph, self.target_device)
        graph.clean_up()

        self.fq_insertion.find_and_replace_pattern(graph)
        graph.clean_up()

        self.fq_propagation.find_and_replace_pattern(graph)
        graph.clean_up()

        self.fq_optimization.find_and_replace_pattern(graph)
        graph.clean_up()

        self.fq_propagation.find_nodes_fq_int(graph)
        graph.clean_up()

        return graph

    def insert_fake_quantize(self, model, ignored_params=None):
        ignored_params_ = preprocess_ignored_params(ignored_params, model)
        for model_dict in model.models:
            self.fq_insertion.ignored_params = ignored_params_[model_dict['name']] if model.is_cascade \
                else ignored_params_
            self._insert_fake_quantize(model_dict['model'])
        return model

    def _remove_fq_nodes(self, graph, node_names, force=False):
        removed_nodes = []
        ops_in_orig_precision = []
        for node_name in node_names:
            if node_name not in removed_nodes:
                fq_nodes, ops = self.fq_removal.find_and_remove_node(graph, node_name, force=force)
                removed_nodes += fq_nodes
                ops_in_orig_precision += ops
        graph.clean_up()

        return removed_nodes, ops_in_orig_precision

    def remove_fq_nodes(self, model, node_names, force=False):
        removed_nodes = []
        ops_in_orig_precision = []
        for model_dict in model.models:
            fq_nodes, ops = self._remove_fq_nodes(model_dict['model'], node_names, force)
            removed_nodes.extend(fq_nodes)
            ops_in_orig_precision.extend(ops)
        return model, removed_nodes, ops_in_orig_precision
