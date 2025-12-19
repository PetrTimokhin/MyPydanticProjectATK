from files.task_2.test_validate_call import *
from files.task_3.const import deals_to_create
from files.task_3.contex_manager import ContextManagerDB
from files.task_3.deals_repository import DealsRepository
from files.task_3.deals_store import DealsStore

db_cont_manage = ContextManagerDB()
deal_repository = DealsRepository(db_cont_manage)


if __name__ == '__main__':
    print('task_2')
    print()
    test_validate_call()
    print()
    print('task_3')
    print()
    deal_repository.deal_models = deals_to_create
    deal_repository.create_deal()
    print(DealsStore().get_store())

