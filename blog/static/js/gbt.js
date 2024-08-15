document.getElementById('input-gbt').addEventListener('input', function () {
    this.value = this.value; // يتم تحديث خاصية value بنفس النص المدخل
});

var myButton = document.getElementById('Button-gbt');

// إضافة مستمع للأحداث للنقر على الزر
myButton.addEventListener('click', function () {
    var inputText = document.getElementById('input-gbt');
    if (inputText.value !== "" && myButton.innerHTML === "ارسال") {
        console.log("re: " + inputText)
        // إنشاء عنصر li جديد
        crate_li(inputText.value)

        ////////////////
        // ارسال رد
        // تحديد عنوان واجهة برمجة التطبيقات
        const apiUrl = 'http://127.0.0.1:5000/app-gbt';

        // إعداد البيانات التي تريد إرسالها
        const requestData = {
            method: 'POST', // أو 'GET' حسب نوع الطلب
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: inputText.value
            }) // بيانات الطلب
        };

        inputText.value = ""
        myButton.innerHTML = "<div class='spener-loading'></div>"

        // إرسال الطلب
        fetch(apiUrl, requestData)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json(); // تحويل الرد إلى JSON
            })
            .then(data => {
                // var data12 = data
                console.log('Success:', data); // التعامل مع البيانات
                // انشاء عنصر
                crate_li(data["message"], true)
                myButton.innerHTML = "ارسال"

            })
            .catch(error => {
                console.error('Error:', error); // التعامل مع الأخطاء
            });

        ////////////////
    }
})

function crate_li(value_t, is_gbt_msg = false) {
    var newListItem = document.createElement('li');
    // يحدد تنسيق الرسال ان كانت لي ام لشات جي بي تي 
    if (is_gbt_msg) {
        newListItem.className = 'card gbt-chat';
    } else {
        newListItem.className = 'card my-chat';

    }
    // إنشاء عنصر div جديد لداخل li
    var newDiv = document.createElement('div');
    newDiv.className = 'card-body';
    newDiv.textContent = value_t;

    // إضافة div إلى li
    newListItem.appendChild(newDiv);

    // الحصول على قائمة ul
    var listChat = document.querySelector('.list-chat');

    // إضافة li إلى ul
    listChat.appendChild(newListItem);
}