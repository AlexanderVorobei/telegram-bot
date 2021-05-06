cd ~
# Создаем виртуальное окружение
virtualenv env
# Активируем виртуальное окружение
source env/scripts/activate
# Клонируем проект
git clone https://github.com/AlexanderVorobei/telegram-bot.git
# Ставим необходимые модули
pip install -r requirements.txt
# Запускаем приложение
python main.py
