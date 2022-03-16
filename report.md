# Установка Virtual Box
Необходимо установить Virtual Box с  **[официального сайта](https://www.virtualbox.org/)**.
После установки на главном экране отобрасяться все виртуальные машины, которые мы можем использовать.<br>
![Info](Assets/main_display.png "main_display" )<br>
# Создание виртуальной машины
Для того, чтобы создать виртуальную машину необходимо в пункте **управление** нажать на кнопку **создать**, 
тогда откроется окно, в котором необходимо указать имя создаваемой машины, выбрать папку для её расположения и указать<br>
![Info](Assets/creating_machine_window.png "creating_machine_window" )<br>
Далее необходимо установить настройки для созданной виртуальной машины. После завершения на главном экране появится созданная виртуальная машина
# Установка Ubuntu Server
Для установки необходимо скачать Ubuntu Server с **[официального сайта](https://ubuntu.com/download/server)**. <br>
Далее необходимо запустить виртуальную машину, на которую хотите установить систему. Появится следующее окно:<br>
![Info](Assets/Install_ubuntu.png "creating_machine_window" ) <br>
Тут необходимо указать загрузочный диск с системой, который был скачан ранее. Далее необходимо выбрать параметры 
установки системы и на следующем окне указать имя пользователя, имя сервера и пароль.<br>
![Info](Assets/username_screen.png "username_screen" ) <br>
Далее будет выполнена установка системы. По завершении которой необходимо перезапустить систему<br>

# Работа с первой машиной
1. С помощью текстового редактора vim меняем имя хоста в файле /etc/hostname на Alexandrov_server<br>
![Info](Assets/hostname1.png "hostname1" ) <br>
   
2. создадим пользователя alexandrov_1 и добавим его в группу sudo<br>
![Info](Assets/creating_alexandrov_1.png "username1" ) <br>

3. Создадим ssh-key на ПК с помощью команды ssh-keygen и подключимся с его помощью к виртуальной машине <br>

![Info](Assets/ssh-key.png "ssh" ) <br>

4. Сконфиурируем виртуальный интерфейс для этого откроем с помощью редактора файл .yaml, который расположен в каталоге /etc/netplan/ и отредактируем его следующим образом:<br>

![Info](Assets/netplan_cfg.png "netplan_cfg" ) <br>
После настройки виртуальные интерфейсы выглядят следующим образом:
![Info](Assets/ip_adrr_1.png "ip_adrr_1" ) <br>

5. отключим в конфигурации netplan enp0s8 и устрановим Python и flask  и вернём настройки netplan обратно<br>

# Работа со второй машиной

1. Сконфигурируем сеть через virtualbox<br>

![Info](Assets/web_2.png "web_2" ) <br>

2. поменяем имя хоста на alexandrovgateway и создадим пользователя alexandrov_2 <br>
![Info](Assets/creating_alexandrov_2.png "alexandrov_2" ) <br>

3. сконфигурируем netplay следующим образом:<br>
![Info](Assets/netplan_cfg_2.png "netplan_cfg_2" ) <br>
После настройки виртуальные интерфейсы выглядят следующим образом:
![Info](Assets/ip_adrr_2.png "ip_adrr_2" ) <br>

# Работа с третьей машиной

1. Сконфигурируем сеть через virtualbox<br>

![Info](Assets/web_3.png "web_3" ) <br>

2. поменяем имя хоста на alexandrovclient и создадим пользователя alexandrov_3 <br>
![Info](Assets/creating_alexandrov_3.png "alexandrov_3" ) <br>

3. сконфигурируем netplay следующим образом:<br>
![Info](Assets/netplan_cfg_3.png "netplan_cfg_3" ) <br>
После настройки виртуальные интерфейсы выглядят следующим образом:
![Info](Assets/ip_adrr_3.png "ip_adrr_3" ) <br>

# Конфигурация маршрутов
Попробуем пингануть интерфейс enp0s8 у alexandrovclient с alexandrovserver<br>
![Info](Assets/ping_failed.png "ping_failed" ) <br>
 Как видно пинг не проходит, потому что эти интерфейсы находяться в разных подсетях.<br>
Настроим переброску пакетов в alexandrov_gateway<br>
![Info](Assets/paste_1_in_forward.png "paste_1_in_forward" ) <br>
теперь у нас получается пингануть 3 машину с первой<br>
![Info](Assets/ping_success.png "paste_1_in_forward" ) <br>
Воспользуемся командой tcpdump, чтобы посмотреть на то, как перебрасываются пакеты в интерфейсах enp0s8 и enp0s9
![Info](Assets/tcpdump_enp0s8.png "tcpdump_enp0se8" ) <br>
![Info](Assets/tcpdump_enp0s9.png "tcpdump_enp0se9" ) <br>
 Теперь нужно сохранить данную настройку изменив в файле /etc/sysctl.conf параметр ip_forward =1<br>
![Info](Assets/ip_forward_1.png "ip_forward_1" ) <br>
Теперь необходимо разрешить переброс только конкретных пакетов по конкретному порту<br>
![Info](Assets/add_iptables.png "add_iptables" ) <br>
Теперь мы не можем пингануть с первой машины третью, потому что вторая выбрасывает не tcp  пакеты<br>
![Info](Assets/ping_failed_2.png "ping_failed_2" ) <br>
Нужно сохранить настройки iptables, чтобы при перезагрузке системы они сохранились.<br>
Для этого воспользуемся командой sudo iptables-save | tee /etc/iptables/rules.v4. Так у нас создасться файл в каталоге /etc/iptables/ с правилами
Теперь при перезагрузке данные правила будут автоматически применяться

# Создание веб-сервера

На alexandrovserver создадим файл app.py, в котором поднимем сервер с помощью Flask framework создадим [файл](application.py)
После чего можем с alexandrovclient послать 3 разных запроса с помощью curl
![Info](Assets/3_request.png "3_request" ) <br>
Как видим, сервер присылает ответы, которые были прописаны на сервере в зависимости от запроса
Перезапустим сервер на порту 5001 и отправим запрос повторно
![Info](Assets/wrongPort.png "reboot_services" ) <br>

Теперь необходимо сделать так, чтобы сервер поднимался при запуске системы автоматически.
Для этого необходимо изменить файл в папке /lib/systemd/systen/web-server.service [следующим образом](configs/Ubuntu_A/web-server.service)
После чего необходимо перезапустить службы и активировать автозагрузку<br>
![Info](Assets/reboot_services.png "reboot_services" ) <br>
