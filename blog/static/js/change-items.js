    // تحويل الناف بار للون الاخضر
    var navElement = document.getElementById('navbar');
    if (navElement) {
        navElement.classList.remove('bg-success');
        navElement.classList.add('bg-primary');
    }
    // لتنفيذ أكواد جافاسكربت بعد تحميل الصفحة بالكامل
    document.addEventListener('DOMContentLoaded', function () {
 
        var buttomElement = document.querySelectorAll('#buttom');

        if (buttomElement) {
            for (let index = 0; index < buttomElement.length; index++) {
                buttomElement[index].classList.remove('btn-success');
                buttomElement[index].classList.add('btn-primary');
            }
        }
    });
