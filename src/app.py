import flet as ft
import random
import json

# --- 1. Данные (как в оригинале) ---
TRANSLATIONS = {
    "Scrooge": "Скрудж", "Christmas": "Рождество", "Carol": "Песнь",
    "Marley": "Марли", "ghost": "призрак", "past": "прошлое",
    "present": "настоящее", "future": "будущее", "happy": "счастливый",
    "sad": "грустный", "cold": "холодный", "warm": "тёплый",
    "heart": "сердце", "soul": "душа", "money": "деньги",
    "work": "работа", "night": "ночь", "day": "день",
    "old": "старый", "good": "хороший", "bad": "плохой",
    "love": "любовь", "fear": "страх", "joy": "радость"
}
TEXT = "Marley was dead Scrooge and Christmas Carol ghost past present future"
WORDS = TEXT.split()

# --- 2. Основное приложение Flet ---
def main(page: ft.Page):
    # Настройки страницы
    page.title = "🎄 Рождественская песнь"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Переменные состояния приложения
    # Список булевых значений: переведено слово или нет
    states = [False] * len(WORDS)
    # Текущий порядок индексов слов (для перемешивания)
    indices_order = list(range(len(WORDS)))

    # --- 3. Элементы интерфейса (виджеты) ---
    
    # Заголовок и подзаголовок
    title = ft.Text("🎄 Интерактивный переводчик", size=32, weight=ft.FontWeight.BOLD)
    subtitle = ft.Text("Чарльз Диккенс «Рождественская песнь»", size=18, italic=True)
    
    # Статус-бар прогресса
    progress_text = ft.Text("Прогресс: 0 / 10", size=16)
    progress_bar = ft.ProgressBar(width=400, value=0.0, color=ft.Colors.GREEN)
    
    # Контейнер для карточек со словами (сетка)
    word_grid = ft.GridView(
        expand=True,
        runs_count=4,  # 4 колонки как в оригинале
        max_extent=150,
        child_aspect_ratio=2.0,
        spacing=10,
        run_spacing=10,
    )
    
    # --- 4. Функция для обновления интерфейса (единственный источник правды) ---
    def refresh_ui():
        """Перерисовывает карточки, обновляет прогресс и сохраняет состояние."""
        # Очищаем старые карточки
        word_grid.controls.clear()
        
        # Создаем карточки в текущем порядке indices_order
        for idx_in_order in indices_order:
            word_raw = WORDS[idx_in_order]
            clean_word = word_raw.strip(".,!?")
            is_translated = states[idx_in_order]
            
            # Определяем текст на кнопке и иконку
            if is_translated:
                display_text = TRANSLATIONS.get(clean_word, clean_word)
                icon = ft.icons.CHECK_CIRCLE
                bg_color = ft.Colors.GREEN_200
                text_color = ft.Colors.BLACK
            else:
                display_text = word_raw
                icon = ft.icons.TOUCH_APP
                bg_color = ft.Colors.GREY_200
                text_color = ft.Colors.BLACK87
            
            # Создаем красивую карточку-кнопку
            card = ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(icon, size=20, color=text_color),
                        ft.Text(
                            display_text,
                            size=16,
                            weight=ft.FontWeight.W_500,
                            color=text_color,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                ),
                bgcolor=bg_color,
                border_radius=10,
                padding=15,
                ink=True,  # Эффект волны при клике
                on_click=lambda e, i=idx_in_order: toggle_word(i),
            )
            word_grid.controls.append(card)
        
        # Обновляем прогресс
        done_count = sum(states)
        total_words = len(WORDS)
        progress_text.value = f"Переведено: {done_count} из {total_words}"
        progress_bar.value = done_count / total_words if total_words else 0
        
        # Сохраняем состояние в локальное хранилище браузера
        page.client_storage.set("app_states", json.dumps(states))
        page.client_storage.set("app_order", json.dumps(indices_order))
        
        page.update()

    # --- 5. Функция переключения слова (клик по карточке) ---
    def toggle_word(index):
        """Меняет состояние конкретного слова."""
        states[index] = not states[index]
        refresh_ui()

    # --- 6. Функции управления (кнопки) ---
    def reset_all(e):
        """Сброс всех переводов."""
        for i in range(len(states)):
            states[i] = False
        refresh_ui()

    def translate_all(e):
        """Перевести всё."""
        for i in range(len(states)):
            states[i] = True
        refresh_ui()

    def shuffle_words(e):
        """Перемешать порядок карточек."""
        random.shuffle(indices_order)
        refresh_ui()
    
    def reset_order(e):
        """Вернуть исходный порядок."""
        nonlocal indices_order
        indices_order = list(range(len(WORDS)))
        refresh_ui()

    # --- 7. Загрузка сохранённого состояния (если есть) ---
    saved_states = page.client_storage.get("app_states")
    saved_order = page.client_storage.get("app_order")
    
    if saved_states:
        try:
            loaded_states = json.loads(saved_states)
            if len(loaded_states) == len(states):
                for i, val in enumerate(loaded_states):
                    states[i] = val
        except:
            pass
    
    if saved_order:
        try:
            loaded_order = json.loads(saved_order)
            if len(loaded_order) == len(indices_order):
                indices_order = loaded_order
        except:
            pass

    # --- 8. Сборка интерфейса (контролы) ---
    control_row1 = ft.Row(
        [
            ft.ElevatedButton("✅ Перевести всё", icon=ft.icons.TRANSLATE, on_click=translate_all),
            ft.ElevatedButton("🔄 Сбросить", icon=ft.icons.RESTART_ALT, on_click=reset_all),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )
    
    control_row2 = ft.Row(
        [
            ft.OutlinedButton("🎲 Перемешать", icon=ft.icons.SHUFFLE, on_click=shuffle_words),
            ft.OutlinedButton("📋 Исходный порядок", icon=ft.icons.REORDER, on_click=reset_order),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )
    
    # Описание (как было в expander)
    how_it_works = ft.Container(
        content=ft.Column([
            ft.Text("📌 Как это работает:", weight=ft.FontWeight.BOLD),
            ft.Text("- Кликайте на карточку для перевода / отмены"),
            ft.Text("- Используйте «Перемешать» для эффективного запоминания"),
            ft.Text("- Прогресс сохраняется автоматически в браузере"),
        ]),
        margin=ft.margin.only(top=20),
        padding=15,
        bgcolor=ft.Colors.BLUE_50,
        border_radius=10,
    )

    # --- 9. Добавляем всё на страницу ---
    page.add(
        title,
        subtitle,
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        progress_text,
        progress_bar,
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        word_grid,
        control_row1,
        control_row2,
        how_it_works,
    )
    
    # Первоначальная отрисовка
    refresh_ui()

# --- 10. Запуск приложения ---
if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
