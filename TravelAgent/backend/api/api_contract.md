# TravelAgent HTTP API 契约

## 1. 创建规划任务

### 方法和路径

- 方法：POST
- 路径：/api/plan-tasks

### 作用

前端发送用户偏好，后端创建规划任务

### 请求

- Content-Type：application/json
- 请求体模型：PlanRequest

请求 JSON 示例：

```json
{
    "destination":"杭州",
    "start_date":"2026-12-10",
    "end_date":"2026-12-11",
    "traveler_account": 2,
    "transport_modes":["公共交通","步行","出租车"],
    "accommodation_types":["酒店"],
    "budget_per_night": 500,
    "special_requirements":"希望行程节奏舒缓，保留午后休息时间"
}
```

### 成功响应

- HTTP 状态码：202 Accepted
- 响应模型：PlanTaskAccepted

响应JSON示例:
```json
{
    "task_id": "task-001"
}
```

## 2.监听任务进度

### 方法和路径

- 方法：GET
- 路径：/api/plan-tasks/{task_id}/events
- 路径参数: task_id,表示要监听的规划任务编号

### 作用

前端使用已有的task_id建立SSE连接，后端持续推送该任务的真实进度，直到任务完成或失败

### 请求

- Accept:text/event-stream
- 请求体：无 SSE请求没有请求体

### 成功响应

- HTTP 状态码: 200 OK
- Content-Type: text/event-stream
- 事件类型：progress、completed、failed

### 连接结束规则

- completed 事件发送后结束连接
- failed 事件发送后结束连接。
- 前端收到 completed 或 failed 后主动关闭 EventSource。
- progress 事件的 progress 范围为 0～99；completed 固定为100。
- current_stage 只能是四个固定 PlanStageId 之一。
- eta_seconds 无法可靠估算时为 null，否则为非负整数。

```json
{
    "type": "progress",
    "task_id": "task-001",
    "progress": 42,
    "current_stage": "select_places_and_stay",
    "eta_seconds": 32
}
```

```json
{
    "type": "completed",
    "task_id": "task-001",
    "progress": 100,
    "result_id": "result-001",
    "summary": {
        "days": 2,
        "nights": 1,
        "place_count": 7,
        "budget_per_night": 500,
        "highlights": ["顺路安排，减少往返"]
    }
}
```

```json
{
    "type": "failed",
    "task_id": "task-001",
    "message": "生成行程时发生错误，请重新规划"
}
```

## 3.查询完整规划结果

### 方法和路径

- 方法：GET
- 路径：/api/plan-results/{result_id}
- 路径参数：result_id, 表示返回结果对应的规划结果编号

### 作用

前端调用这个接口返回规划结果
前端根据 completed 事件返回的 result_id，查询后端已经保存的完整 PlanResult。

### 请求

- Accept: application/json
- 请求体: 无

### 成功响应

- HTTP 状态码： 200 OK
- Content-Type: application/json
- 响应模型：PlanResult
- 完整响应示例：[draft.json](./draft.json)

### 一致性规则

- 后端必须先保存 PlanResult，再发送 completed 事件。
- 路径中的 result_id 必须与返回结果中的 PlanResult.result_id 相同。

## 4.通用错误响应

- 422 Unprocessable Content POST请求内容不合法
- VALIDATION_ERROR
- 404 Not Found SSE的task_id不存在/查询的result_id不存在/已失效
- TASK_NOT_FOUND RESULT_NOT_FOUND
- 统一错误JSON至少包含code 和 message

```json
{
    "code": "TASK_NOT_FOUND",
    "message": "未找到对应的规划任务"
}
```