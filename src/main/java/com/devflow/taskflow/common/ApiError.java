package com.devflow.taskflow.common;

import java.util.Map;

public record ApiError(
        String code,
        String message,
        Map<String, String> fieldErrors,
        String traceId
) {
}
