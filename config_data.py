"""
Конфигурационные данные для агентов системы
Содержит информацию о доступных датах отпуска и бюджете на повышение
"""

# Доступные даты для отпуска (в формате YYYY-MM-DD)
AVAILABLE_VACATION_DATES = [
    "2024-12-23", "2024-12-24", "2024-12-25", "2024-12-26", "2024-12-27", "2024-12-30", "2024-12-31",
    "2025-01-02", "2025-01-03", "2025-01-06", "2025-01-07", "2025-01-08", "2025-01-09", "2025-01-10",
    "2025-01-13", "2025-01-14", "2025-01-15", "2025-01-16", "2025-01-17", "2025-01-20", "2025-01-21",
    "2025-01-22", "2025-01-23", "2025-01-24", "2025-01-27", "2025-01-28", "2025-01-29", "2025-01-30", "2025-01-31"
]

# Доступный бюджет для повышения зарплаты (в рублях)
SALARY_INCREASE_BUDGET = {
    "total_available": 500000,  # Общий доступный бюджет
    "max_per_employee": 50000,  # Максимальное повышение на сотрудника
    "min_increase": 10000       # Минимальное повышение
}

# Функция для получения актуальных данных
def get_current_config():
    """
    Возвращает текущую конфигурацию в удобном для агентов формате
    """
    return {
        "vacation_dates": AVAILABLE_VACATION_DATES,
        "salary_budget": SALARY_INCREASE_BUDGET
    }

# Функция для проверки доступности даты отпуска
def is_vacation_date_available(date_str):
    """
    Проверяет, доступна ли дата для отпуска
    """
    if date_str in AVAILABLE_VACATION_DATES:
        return True, "Дата доступна для отпуска"
    else:
        return False, "Дата недоступна для отпуска"

# Функция для проверки бюджета на повышение
def check_salary_increase_budget(requested_amount):
    """
    Проверяет, достаточно ли бюджета для повышения зарплаты
    """
    if requested_amount <= SALARY_INCREASE_BUDGET["max_per_employee"]:
        if requested_amount <= SALARY_INCREASE_BUDGET["total_available"]:
            return True, f"Бюджет достаточен. Доступно: {SALARY_INCREASE_BUDGET['total_available']} руб."
        else:
            return False, f"Недостаточно общего бюджета. Доступно: {SALARY_INCREASE_BUDGET['total_available']} руб."
    else:
        return False, f"Превышен лимит на сотрудника. Максимум: {SALARY_INCREASE_BUDGET['max_per_employee']} руб."
