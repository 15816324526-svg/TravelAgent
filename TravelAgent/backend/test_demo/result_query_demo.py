import asyncio
from pathlib import Path

from main import get_plan_result, plan_results
from model.plan_model import PlanResult

#创建一个Path路径对象 然后读取这个路径指向的文件，按utf-8
json_text = Path("draft.json").read_text(encoding="utf-8")

#对着Pydantic模型创建对象plan_result，但是要经过
#pydantic自带的校验方法:.model_validate_json
plan_result = PlanResult.model_validate_json(json_text)

#把plan_result这个结果放进内存结果表
plan_results[plan_result.result_id] = plan_result

#执行完成后不需要返回业务数据
async def main() -> None:
    #调用结果查询路由函数
    returned_result = await get_plan_result(plan_result.result_id)

    #assert+条件 如果false就抛出AssertionError
    #查询结果编号 ==在比较结果编号的值
    assert returned_result.result_id == plan_result.result_id
    #is  → 判断是否指向内存中的同一个对象
    assert returned_result is plan_result

    print(returned_result.result_id)
    print(returned_result.title)

if __name__ == "__main__":
    asyncio.run(main())


