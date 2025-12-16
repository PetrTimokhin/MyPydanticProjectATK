from typing import Dict, List, Any, Optional
from pydantic import BaseModel, ValidationError

from files.task_3.contex_manager import ContextManagerDB
from files.task_3.schemas import Deal


class DealsRepository:
    def __init__(self,
                 db_context_manager: ContextManagerDB,
                 deal_models: Optional[Deal | str] = None):
        self.__deal_models = deal_models
        self.__db_context_manager = db_context_manager

    # Модель сделки (геттер/сеттер/делиттер)
    @property
    def deal_models(self):
        return self.__deal_models

    @deal_models.setter
    def deal_models(self, lst: [Deal, str]):
        self.__deal_models = lst


    @deal_models.deleter
    def deal_models(self):
        self.__deal_models.clear()

    def create_deal(self) -> None:
        """Создание одной или нескольких сделок без прерывания при ошибке."""
        errors = []
        with self.__db_context_manager as store:
            current = store.get_store()

            for deal in self.__deal_models:
                try:
                    if isinstance(deal, Deal):
                        current.append(deal)
                        print(f'Сделка id:{deal.id} прошла!')
                    current.append(Deal.model_validate_json(deal))
                except ValidationError as e:
                    errors.append(str(e))

            store.set_store(current)

            if errors:
                print("\n[CREATE DEAL ERRORS]")
                for e in errors:
                    print(e)


    def get_deals(self) -> List[BaseModel]:
        """get_deals – возвращает сделки как список Pydantic схем."""
        with self.__db_context_manager as store:
            return store.get_store()


    def get_deals_dicts(self) -> List[Dict[str, Any]]:
        """get_deals_dicts – возвращает сделки как список словарей."""
        with self.__db_context_manager as store:
            return [d.model_dump() for d in store.get_store()]


    def get_deal(self, deal_id: int) -> Optional[BaseModel]:
        """get_deal – возвращает одну сделку"""
        with self.__db_context_manager as store:
            for deal in store.get_store():
                if deal.id == deal_id:
                    return deal
        return None


    def delete_deal(self, deal_id: int) -> bool:
        """delete_deal – удаляет одну сделку."""
        with self.__db_context_manager as store:
            deals = store.get_store()
            for i, deal in enumerate(deals):
                if deal.id == deal_id:
                    del deals[i]
                    store.set_store(deals)
                    return True
        return False


    def update_deal(self,
                    deal_id: int,
                    user_id: int | None,
                    new_data: dict
                    ) -> None:
        """update_deal – позволяет обновить сделку ИЛИ данные пользователя связанного со сделкой."""
        with self.__db_context_manager as store:
            deals = store.get_store()

            for i, deal in enumerate(deals):
                if deal.id == deal_id:
                    dct_deal = deal.model_dump()
                    if user_id:
                        for j, user in enumerate(dct_deal['persons_in_charge']):
                            if user['id'] == user_id:
                                dct_deal['persons_in_charge'][j] = new_data
                                deals.append(Deal.model_validate(dct_deal))
                    dct_deal.update(new_data)
                    deals.append(Deal.model_validate(dct_deal))
            store.set_store(deals)

