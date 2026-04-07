class OrderSplitHelper:
    """
    Вспомогательный класс для работы с автоматической разбивкой заказов.

    Система автоматически разбивает заказы на максимум 4 группы по типу материалов:
    - Группа 1: Material (обычные торговые коды)
    - Группа 2: HEXAdditions (ЗИП и изоляция на ПТО)
    - Группа 3: TDU, AutoShield, BTP (производственные материалы)
    - Группа 4: HEX, Pump (разборные ПТО и насосы)
    """

    @staticmethod
    def calculate_expected_orders_count(order_lines: list) -> int:
        """
        Вычисляет ожидаемое количество заказов на основе типов материалов в запросе.

        :param order_lines: Список объектов orderLines из запроса Order/Create.
                           Каждый объект должен содержать поле 'lineType'.
        :return: Ожидаемое количество заказов (от 1 до 4).

        Example:
            order_lines = [
                {"lineType": "Material"},
                {"lineType": "HEX"}
            ]
            result = OrderSplitHelper.calculate_expected_orders_count(order_lines)
            # result = 2
        """
        line_types = [line['lineType'] for line in order_lines]
        active_groups = OrderSplitHelper._get_active_groups(line_types)
        return len(active_groups)

    @staticmethod
    def _get_active_groups(line_types: list) -> set:
        """
        Определяет какие группы материалов активны в запросе.

        Логика группировки:
        - Группа 1: lineType = "Material"
        - Группа 2: lineType = "HEXAdditions"
        - Группа 3: lineType in ["TDU", "AutoShield", "BTP"]
        - Группа 4: lineType in ["HEX", "Pump"]

        :param line_types: Список значений lineType из orderLines.
        :return: Множество номеров активных групп (от 1 до 4).

        Example:
            line_types = ["Material", "HEX", "TDU"]
            groups = OrderSplitHelper._get_active_groups(line_types)
            # groups = {1, 3, 4}
        """
        groups = set()

        if "Material" in line_types:
            groups.add(1)

        if "HEXAdditions" in line_types:
            groups.add(2)

        if any(lt in ["TDU", "AutoShield", "BTP"] for lt in line_types):
            groups.add(3)

        if any(lt in ["HEX", "Pump"] for lt in line_types):
            groups.add(4)

        return groups

    @staticmethod
    def extract_base_offer_number(offer_number: str) -> str:
        """
        Извлекает базовый номер оффера без постфикса.

        :param offer_number: Полный номер оффера (например, "PQ04815549-1").
        :return: Базовый номер без постфикса (например, "PQ04815549").

        Example:
            base = OrderSplitHelper.extract_base_offer_number("PQ04815549-1")
            # base = "PQ04815549"

            base = OrderSplitHelper.extract_base_offer_number("PQ04815549")
            # base = "PQ04815549"
        """
        if '-' in offer_number:
            return offer_number.rsplit('-', 1)[0]
        return offer_number

    @staticmethod
    def validate_offer_numbers_have_same_base(offer_numbers: list) -> bool:
        """
        Проверяет что все номера офферов имеют одинаковую базу.

        Все заказы созданные из одного запроса должны иметь общий базовый номер
        с разными постфиксами (-1, -2, -3, -4).

        :param offer_numbers: Список номеров офферов из ответа.
        :return: True если все номера имеют одну базу, False в противном случае.

        Example:
            offer_numbers = ["PQ04815549-1", "PQ04815549-2", "PQ04815549-3"]
            result = OrderSplitHelper.validate_offer_numbers_have_same_base(offer_numbers)
            # result = True

            offer_numbers = ["PQ04815549-1", "PQ04815550-1"]
            result = OrderSplitHelper.validate_offer_numbers_have_same_base(offer_numbers)
            # result = False
        """
        if not offer_numbers:
            return False

        base_numbers = [OrderSplitHelper.extract_base_offer_number(num) for num in offer_numbers]
        return len(set(base_numbers)) == 1

    @staticmethod
    def validate_offer_ids_unique(offer_ids: list) -> bool:
        """
        Проверяет уникальность всех offerId в ответе.

        Каждый созданный заказ должен иметь уникальный offerId.

        :param offer_ids: Список offerId из ответа.
        :return: True если все offerId уникальны, False если есть дубликаты.

        Example:
            offer_ids = ["uuid1", "uuid2", "uuid3"]
            result = OrderSplitHelper.validate_offer_ids_unique(offer_ids)
            # result = True

            offer_ids = ["uuid1", "uuid2", "uuid1"]
            result = OrderSplitHelper.validate_offer_ids_unique(offer_ids)
            # result = False
        """
        return len(offer_ids) == len(set(offer_ids))

    @staticmethod
    def validate_offer_numbers_unique(offer_numbers: list) -> bool:
        """
        Проверяет уникальность всех offerNumber в ответе.

        Каждый созданный заказ должен иметь уникальный offerNumber.

        :param offer_numbers: Список offerNumber из ответа.
        :return: True если все offerNumber уникальны, False если есть дубликаты.

        Example:
            offer_numbers = ["PQ04815549-1", "PQ04815549-2"]
            result = OrderSplitHelper.validate_offer_numbers_unique(offer_numbers)
            # result = True

            offer_numbers = ["PQ04815549-1", "PQ04815549-1"]
            result = OrderSplitHelper.validate_offer_numbers_unique(offer_numbers)
            # result = False
        """
        return len(offer_numbers) == len(set(offer_numbers))