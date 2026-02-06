from selenium.webdriver.common.by import By


class CartSharedPageLocators:
    """Локаторы страницы С вами поделились корзиной"""
    LOCATOR_HEADER_MODAL_SHARED_CART_WITH_YOU = (
        By.XPATH, "//span[@class='fs-5 fw-bold' and contains(text(), "
                  "'С вами поделились корзиной, но в вашей корзине уже есть товары')]"
    )  # Заголовок в модалке "С вами поделились корзиной, но в вашей корзине уже есть товары "
    LOCATOR_BTN_CLEAN_AND_ADD_IN_MODAL_SHARED_CART_WITH_YOU = (
        By.XPATH, "//button[contains(text(), 'Очистить и добавить')]"
    )  # Кнопка Очистить и добавить в модалке "С вами поделились корзиной, но в вашей корзине уже есть товары"
    LOCATOR_ARTICLE = (
        By.XPATH, "//a[@class='fw-bold fs-6 text-reset border-0 text-decoration-none']//span[@class='text-break']"
    )  # Артикул на странице
    LOCATOR_BTN_ADD_SALES = (By.XPATH, "//button[contains(text(), ' Добавить в корзину ')]")
    # Кнопка Добавить в корзину
    LOCATOR_QUANTITY_IN_CART_ON_CART_ICON = (By.XPATH, "//span[@data-cart-count and contains(@class, 'd-none')]"
                                             )  # Количество в корзине на иконке Корзина
