from files.task_3.schemas import Deal

deal_json_1 = ('{"title": "Сделка",'
               ' "comment": "Коммент",'
               ' "created_at": "10-10-2025",'
               ' "persons_in_charge": [{"name": "Petr1", "age": 43, "email": "petr@example.com", "phone_number": "+7 (000) 000-00-00"}],'
               ' "deal_type": 1}')

deal_json_2 = ('{"title": "Сделка",'
               ' "comment": "Коммент",'
               ' "created_at": "10-10-2025",'
               ' "persons_in_charge": [{"name": "Petr2", "age": 43, "email": "petr@example.com", "phone_number": "+7 (000) 000-00-00"}],'
               ' "deal_type": 1}')

deal_json_wrong = ('{"title": "Сделка",'
               ' "comment": "Коммент",'
               ' "created_at": "10-10-2025",'
               ' "persons_in_charge": [{"name": "Petr2", "age": "forty", "email": "petr@example.com", "phone_number": "+7 (000) 000-00-00"}],'
               ' "deal_type": 1}')

deals_to_create = [Deal.model_validate_json(deal_json_1),
                   Deal.model_validate_json(deal_json_2),
                   deal_json_wrong]
