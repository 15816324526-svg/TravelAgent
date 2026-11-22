//前端发给后端的偏好
export interface PlanRequest {
    destination: string
    start_date: string
    end_date: string
    traveler_account: number
    transport_modes: string[]
    accommodation_types: string[]
    budget_per_night:number
    special_requirements: string
}

//固定阶段 ID
export type PlanStageId =
  | 'understand_preferences' //理解旅行偏好
  | 'select_places_and_stay'  //筛选景点与住宿区域
  | 'optimize_route'         //优化路线与交通衔接
  | 'build_itinerary'        //整理专属行程

//任务创建响应 后端立即返回的任务编号
export interface PlanTaskAccepted {
    task_id: string
}

//规划中的进度事件
export interface PlanProgressEvent {
    type: 'progress'  //事件种类
    task_id: string   //属于哪个任务
    progress: number  //后端计算的真实进度，范围为 0～99
    current_stage: PlanStageId  //当前真实阶段
    eta_seconds: number | null  //预计剩余秒数；无法估算时为 null。
}

//完成摘要
export interface PlanResultSummary {
    days: number
    nights: number
    place_count: number
    budget_per_night: number
    highlights: string[]
}

//完成事件
export interface PlanCompletedEvent {
    type: 'completed'
    task_id: string
    progress: 100
    result_id: string
    summary:PlanResultSummary
}

//失败事件
export interface PlanFailedEvent {
    type: 'failed'
    task_id: string
    message: string
}

//合并所有 SSE 事件  后端稍后发送回来的进度或者结果
export type PlanTaskEvent = 
 | PlanProgressEvent
 | PlanCompletedEvent
 | PlanFailedEvent