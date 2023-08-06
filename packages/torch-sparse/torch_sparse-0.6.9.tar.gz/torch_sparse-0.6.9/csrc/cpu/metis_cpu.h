#pragma once

#include <torch/extension.h>

torch::Tensor partition_cpu(torch::Tensor rowptr, torch::Tensor col,
                            torch::optional<torch::Tensor> optional_value,
                            int64_t num_parts, bool recursive);

torch::Tensor mt_partition_cpu(torch::Tensor rowptr, torch::Tensor col,
                               torch::optional<torch::Tensor> optional_value,
                               int64_t num_parts, bool recursive,
                               int64_t num_workers);
