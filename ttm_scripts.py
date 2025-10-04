# ttm_scripts.py - Полная библиотека скриптов для ThaiTicketMajor

def get_script_1():
    """Подтверждение условий"""
    return """
// 1. confirm-terms.js
function isCheckboxChecked() {
    return document.getElementById("rdagree").checked;
}
function clickCheckboxAndProceed() {
    const checkbox = document.getElementById("rdagree");
    const button = document.getElementById("btn_verify");
    if (!isCheckboxChecked()) {
        checkbox.click();
        const checkInterval = setInterval(() => {
            if (isCheckboxChecked()) {
                clearInterval(checkInterval);
                button.click();
            }
        }, 100);
    } else {
        button.click();
    }
}
clickCheckboxAndProceed();
"""

def get_script_2(day="Sat"):
    """Выбор даты показа"""
    return f"""
// 2. select-show-date.js
const dayToSelect = '{day}';
function selectShowDate(day) {{
    const selectBox = document.getElementById('rdId');
    if (selectBox) {{
        const options = selectBox.querySelectorAll('option');
        let found = false;
        options.forEach(option => {{
            if (option.textContent.includes(day)) {{
                selectBox.value = option.value;
                selectBox.dispatchEvent(new Event('change'));
                found = true;
                console.log('Выбран день: ' + day);
            }}
        }});
        if (!found) {{
            console.error('День не найден: ' + day);
        }}
    }} else {{
        console.error('Элемент выбора даты не найден');
    }}
}}
selectShowDate(dayToSelect);
"""

def get_script_3a():
    """Выбор зоны Stand A"""
    return """
// 3. Alter-select-zone-A.js
function clickStandingZone() {
    const areaElements = document.querySelectorAll('area[href*="#A"][onclick*="selectzone"]');
    for (let area of areaElements) {
        if (area.getAttribute('href').includes('#A') || area.getAttribute('onclick').includes('#A')) {
            const event = new MouseEvent('click', { bubbles: true, cancelable: true });
            if (area.onclick) {
                area.onclick(event);
            } else {
                const onclickAttr = area.getAttribute('onclick');
                if (onclickAttr) {
                    try {
                        eval(onclickAttr);
                    } catch (e) {
                        console.error('Ошибка:', e);
                    }
                }
            }
            console.log('Клик по зоне A выполнен');
            return;
        }
    }
    console.error('Зона A не найдена');
}
clickStandingZone();
"""

def get_script_3b():
    """Выбор зоны Stand B"""
    return """
// 3. Alter-select-zone-B.js
function clickStandingZoneB() {
    const areaElements = document.querySelectorAll('area[href*="#BS"][onclick*="selectzone"]');
    for (let area of areaElements) {
        if (area.getAttribute('href').includes('#BS') || area.getAttribute('onclick').includes('#BS')) {
            const event = new MouseEvent('click', { bubbles: true, cancelable: true });
            if (area.onclick) {
                area.onclick(event);
            } else {
                const onclickAttr = area.getAttribute('onclick');
                if (onclickAttr) {
                    try {
                        eval(onclickAttr);
                    } catch (e) {
                        console.error('Ошибка:', e);
                    }
                }
            }
            console.log('Клик по зоне B выполнен');
            return;
        }
    }
    console.error('Зона B не найдена');
}
clickStandingZoneB();
"""

def get_script_3_general(zone):
    """Выбор зоны SC, SD, SM, SL"""
    return f"""
// 3.select-zone-copy.js
const zonePrefix = '{zone}';
const button = document.getElementById('popup-avail');
if (button) {{
    button.click();
    
    // Ждем загрузки данных
    setTimeout(() => {{
        const rows = document.querySelectorAll('tr');
        let bestRow = null;
        let maxSeats = 0;
        
        rows.forEach(row => {{
            const zoneElement = row.querySelector('td:nth-child(1) a');
            const seatsElement = row.querySelector('td:nth-child(2) a');
            
            if (zoneElement && seatsElement) {{
                const zoneId = zoneElement.id;
                const seatsCount = parseInt(seatsElement.textContent, 10);
                
                if (zoneId.startsWith(zonePrefix) && seatsCount > maxSeats) {{
                    maxSeats = seatsCount;
                    bestRow = row;
                }}
            }}
        }});
        
        if (bestRow) {{
            bestRow.click();
            const zoneId = bestRow.querySelector('td:nth-child(1) a').id;
            console.log('Выбрана зона: ' + zoneId + ' с ' + maxSeats + ' местами');
            
            // Вызываем функцию перехода, если она существует
            if (typeof gonextstep === 'function') {{
                gonextstep('fixed.php', zoneId, new Event('click'));
            }}
        }} else {{
            console.error('Зона ' + zonePrefix + ' не найдена');
        }}
    }}, 1000);
}} else {{
    console.error('Кнопка выбора зоны не найдена');
}}
"""

def get_script_4_stand(ticket_count="6"):
    """Выбор количества билетов для Stand A/B"""
    return f"""
// 4.AlterSeatsCount.js
function setSelectValue(selectId, value) {{
    const select = document.getElementById(selectId);
    if (select) {{
        select.value = value;
        ['change', 'input', 'click'].forEach(eventType => {{
            select.dispatchEvent(new Event(eventType, {{ bubbles: true }}));
        }});
        console.log('Выбрано ' + value + ' билетов');
        
        // Нажимаем кнопку Book Now
        setTimeout(() => {{
            const bookNowButton = document.getElementById('booknow');
            if (bookNowButton) {{
                ['mouseover', 'mousedown', 'mouseup', 'click'].forEach(eventType => {{
                    bookNowButton.dispatchEvent(new Event(eventType, {{ bubbles: true }}));
                }});
                console.log('Кнопка Book Now нажата');
            }} else {{
                console.error('Кнопка Book Now не найдена');
            }}
        }}, 500);
    }} else {{
        console.error('Элемент выбора количества билетов не найден');
    }}
}}
setSelectValue('book_cnt', '{ticket_count}');
"""

def get_script_4_general(ticket_count="6"):
    """Выбор мест для зон SC, SD, SM, SL"""
    return f"""
// 4.select-seats.js
let selectedSeats = [];
const requiredSeats = {ticket_count};

function closeAlertIfNeeded() {{
    let alertButton = document.querySelector("button.btn-red.w-auto[onclick='MessageClose()']");
    if (alertButton) {{
        alertButton.click();
    }}
}}

function areSeatsAdjacent(seats) {{
    if (seats.length < requiredSeats) return false;
    
    const rows = seats.map(seat => seat.split('-')[0]);
    const uniqueRows = [...new Set(rows)];
    
    if (uniqueRows.length !== 1) return false;
    
    const seatNumbers = seats.map(seat => parseInt(seat.split('-')[1], 10));
    seatNumbers.sort((a, b) => a - b);
    
    for (let i = 1; i < seatNumbers.length; i++) {{
        if (seatNumbers[i] !== seatNumbers[i - 1] + 1) return false;
    }}
    return true;
}}

function selectAdjacentSeats() {{
    let rows = document.querySelectorAll("#tableseats tbody tr");
    let seatsFound = false;
    let totalSeats = 0;
    let noSeatsFound = true;
    
    for (let i = 0; i < rows.length; i++) {{
        let columns = rows[i].querySelectorAll("td");
        let adjacentSeats = [];
        
        for (let j = 1; j < columns.length; j++) {{
            let seatDiv = columns[j].querySelector("div.seatuncheck");
            let seatId = columns[j].getAttribute("title");
            
            if (seatDiv && !columns[j].classList.contains("not-available")) {{
                adjacentSeats.push(seatId);
                
                if (adjacentSeats.length === requiredSeats) {{
                    if (areSeatsAdjacent(adjacentSeats)) {{
                        adjacentSeats.forEach(seat => {{
                            let seatElement = document.getElementById(`checkseat-${{seat}}`);
                            if (seatElement && !seatElement.classList.contains("seatchecked")) {{
                                seatElement.click();
                            }}
                        }});
                        
                        setTimeout(() => {{
                            closeAlertIfNeeded();
                            
                            let selectedSeatElements = adjacentSeats.every(seat => {{
                                let seatElement = document.getElementById(`checkseat-${{seat}}`);
                                return seatElement && seatElement.classList.contains("seatchecked");
                            }});
                            
                            if (selectedSeatElements) {{
                                console.log("Выбраны соседние места");
                                
                                setTimeout(() => {{
                                    let bookNowButton = document.querySelector('a#booknow');
                                    if (bookNowButton) {{
                                        bookNowButton.click();
                                        console.log('Кнопка Book Now нажата');
                                    }}
                                }}, 500);
                                
                                selectedSeats = adjacentSeats;
                                seatsFound = true;
                                return;
                            }} else {{
                                adjacentSeats.forEach(seat => {{
                                    let seatElement = document.getElementById(`checkseat-${{seat}}`);
                                    if (seatElement && seatElement.classList.contains("seatchecked")) {{
                                        seatElement.click();
                                    }}
                                }});
                                console.log("Места недоступны, ищем другие");
                                adjacentSeats.shift();
                                selectAdjacentSeats();
                            }}
                        }}, 500);
                        
                        return;
                    }} else {{
                        adjacentSeats.shift();
                    }}
                }}
            }}
        }}
        
        if (seatsFound) {{
            noSeatsFound = false;
            break;
        }}
        
        totalSeats += adjacentSeats.length;
    }}
    
    if (noSeatsFound) {{
        console.log("Соседние места не найдены, обновляем страницу");
        location.reload();
    }} else {{
        console.log("Продолжаем поиск мест");
        setTimeout(selectAdjacentSeats, 500);
    }}
}}

selectAdjacentSeats();
"""

def get_script_5(names):
    """Заполнение данных имен"""
    name1, name2, name3, name4, name5, name6 = names
    return f"""
// 5.fill-details.js
function clickAndFillField(selector, value, description) {{
    const field = document.querySelector(selector);
    if (!field) {{
        console.error('Поле не найдено: ' + description);
        return false;
    }}
    
    field.click();
    field.focus();
    
    setTimeout(() => {{
        field.value = '';
        field.value = value;
        
        const events = ['input', 'change', 'keydown', 'keypress', 'keyup', 'blur'];
        events.forEach(eventType => {{
            field.dispatchEvent(new Event(eventType, {{ bubbles: true }}));
        }});
        
        console.log(description + ' заполнено: ' + value);
    }}, 100);
    
    return true;
}}

// Заполняем поля
setTimeout(() => {{
    clickAndFillField('#txt_firstname_0', '{name1}', 'Поле 1');
    
    setTimeout(() => {{
        clickAndFillField('#txt_firstname_1', '{name2}', 'Поле 2');
        
        setTimeout(() => {{
            clickAndFillField('#txt_firstname_2', '{name3}', 'Поле 3');
            
            setTimeout(() => {{
                clickAndFillField('#txt_firstname_3', '{name4}', 'Поле 4');
                
                setTimeout(() => {{
                    clickAndFillField('#txt_firstname_4', '{name5}', 'Поле 5');
                    
                    setTimeout(() => {{
                        clickAndFillField('#txt_firstname_5', '{name6}', 'Поле 6');
                        
                        // Нажимаем кнопку Save
                        setTimeout(() => {{
                            const saveButton = document.querySelector('#btn_regionw, input[value="Save"]');
                            if (saveButton) {{
                                saveButton.click();
                                console.log('Кнопка Save нажата');
                            }} else {{
                                console.error('Кнопка Save не найдена');
                            }}
                        }}, 500);
                        
                    }}, 200);
                }}, 200);
            }}, 200);
        }}, 200);
    }}, 200);
}}, 300);
"""

def get_script_6():
    """Подтверждение оплаты"""
    return """
// 6.AlterPred3DS.js
async function automateBooking() {
    function clickElement(selector, description, attempts = 10, delay = 500) {
        return new Promise((resolve) => {
            let tries = 0;
            function tryClick() {
                tries++;
                const element = document.querySelector(selector);
                if (element) {
                    ['mouseover', 'mousedown', 'mouseup', 'click'].forEach(eventType => {
                        element.dispatchEvent(new Event(eventType, { bubbles: true }));
                    });
                    console.log(description + ' кликнут');
                    resolve(true);
                } else if (tries < attempts) {
                    setTimeout(tryClick, delay);
                } else {
                    console.error(description + ' не найден');
                    resolve(false);
                }
            }
            tryClick();
        });
    }

    function checkCheckbox(selector, description) {
        const checkbox = document.querySelector(selector);
        if (checkbox && !checkbox.checked) {
            checkbox.click();
            console.log(description + ' отмечен');
        }
    }

    if (await clickElement('#btn_pickup', 'Самовывоз')) {
        setTimeout(async () => {
            if (await clickElement('#btn_creditcard', 'Оплата картой')) {
                setTimeout(() => {
                    checkCheckbox('#ticket-protect-mobile', 'Защита билета');
                    setTimeout(() => {
                        checkCheckbox('#check-agree', 'Согласие');
                        setTimeout(() => {
                            clickElement('#btn_confirm', 'Подтверждение оплаты');
                        }, 500);
                    }, 500);
                }, 500);
            }
        }, 500);
    }
}
automateBooking();
"""

# Функция для получения скрипта по номеру шага и настройкам
def get_script_for_step(step, settings):
    """Возвращает скрипт для указанного шага на основе настроек"""
    zone = settings.get("zone", "Stand A")
    day = settings.get("day", "Sat")
    ticket_count = settings.get("ticket_count", "6")
    names = settings.get("names", ["Chiraphat chaikhuntod", "Ya Eby Tvoyu Mat", "32131 3231", "", "", ""])
    
    if step == 1:
        return get_script_1()
    elif step == 2:
        return get_script_2(day)
    elif step == 3:
        if zone == "Stand A":
            return get_script_3a()
        elif zone == "Stand B":
            return get_script_3b()
        else:
            return get_script_3_general(zone)
    elif step == 4:
        if zone in ["Stand A", "Stand B"]:
            return get_script_4_stand(ticket_count)
        else:
            return get_script_4_general(ticket_count)
    elif step == 5:
        if zone not in ["Stand A", "Stand B"]:
            return get_script_5(names)
        else:
            return "// Пропуск шага 5 (не требуется для Stand A/B)"
    elif step == 6:
        return get_script_6()
    else:
        return "// Неизвестный шаг"