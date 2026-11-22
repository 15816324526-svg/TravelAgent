//TS=JS+数据类型说明

//导入类型
import type { 
    PlanRequest,
    PlanTaskAccepted,
    PlanTaskEvent
 } from '../types/plan'

//模拟配置
const MOCK_SUBMIT_DELAY_MS = 1500
const SHOULD_SUBMIT_FAIL = false
const SHOULD_TASK_FAIL = false

function wait(milliseconds: number): Promise<void> {
    return new Promise((resolve) => {
        window.setTimeout(resolve, milliseconds)
    })
}

//创建任务，发送偏好后马上返回任务编号
//export允许其他文件使用这个函数
//调用异步时会获得一个Promise（凭证）
//request是传入参数名称，类型是PlanRequest，说明传入的对象格式要符合PlanRequest
//返回类型是PlanTaskAccepted但是被Promise包住，说明可以等待
export async function submitPlanRequest(
    request:PlanRequest
):Promise<PlanTaskAccepted> {
    //await-等待真正的结果
    await wait(MOCK_SUBMIT_DELAY_MS)

    //检查模拟失败，也就是任务创建失败时要执行
    if(SHOULD_SUBMIT_FAIL) { 
        //new Error（）创建一个错误对象 ，throw把错误抛出去
        throw new Error('创建规划任务失败，请稍后重试')
    }

    //生成任务Id
    const taskId = `mock-task-${Date.now()}`

    //把请求打印到console浏览器开发者工具中
    console.log('模拟提交规划请求:',request)
    console.log('模拟任务 ID ：', taskId)

    return {
        task_id: taskId
    }
}

//监听任务/模拟事件
//立即安排好未来会要发生的事情，返回一个取消函数
export function subscribeToPlanTask(
    taskId: string, //表示要监听哪个任务
    //接收event参数，类型是PlanTaskEvent,表示函数执行完不需要返回结果
    onEvent: (event: PlanTaskEvent) => void  
): () => void {
    //Array<类型>=[{},{},{},{}]
    const scheduledEvents: Array<{
        delay: number
        event: PlanTaskEvent
    } > = [
        {
            delay: 1000,
            event: {
                type: 'progress',
                task_id: taskId,
                progress: 18,
                current_stage: 'understand_preferences',
                eta_seconds: 45
            }
        },
        {
            delay: 2500,
            event: {
                type: 'progress',
                task_id: taskId,
                progress: 42,
                current_stage: 'select_places_and_stay',
                eta_seconds: 32
            }
        },
        {
            delay: 4000,
            event: {
                type: 'progress',
                task_id: taskId,
                progress: 68,
                current_stage: 'optimize_route',
                eta_seconds: 20
            }
        },
        {
            delay: 5500,
            event: {
                type: 'progress',
                task_id: taskId,
                progress: 90,
                current_stage: 'build_itinerary',
                eta_seconds: 8
            }
        }
    ]
    //数组定义完成

    //决定最后成功或者失败
    if (SHOULD_TASK_FAIL) {
        //push()表示往数组末尾增加一个元素
        scheduledEvents.push({
            delay: 7000,
            event: {
                type: 'failed',
                task_id: taskId,
                message: '生成行程时发生错误，请重新规划'
            }
        })
    } else {
        scheduledEvents.push({
          delay: 7000,
          event: {
            type: 'completed',
            task_id: taskId,
            progress: 100,
            result_id: 'mock-result-001',
            summary: {
              days: 2,
              nights: 1,
              place_count: 7,
              budget_per_night: 500,
              highlights: [
                '顺路安排，减少往返折腾',
                '每日步行约 6–7 千步',
                '保留午餐与午后休息时间',
                '附交通建议、天气与住宿参考'
          ]
        }
      }
    })
    }

    //map（）安排定时器
    //map()依次处理数组元素并生成新数组
    const timeoutIds = scheduledEvents.map(({ delay,event }) => {
        //每次调用setTimeout()都会返回一个编号，保存在timeoutIds
        return window.setTimeout(() => {
            onEvent(event)
        },delay)
    })

    //返回取消函数
    return () => {
        //forEach()把每个数组编号取出来
        timeoutIds.forEach((timeoutId) => {
            window.clearTimeout(timeoutId)
        })
    }
}

//
