window.onload = function () {
    `""""""""انشائ زر الترجمة""""""""`
    // قائمة الخصائص
    const targetElement = document.getElementById('cke_1_top');
    //انشائ زر الترجمة
    const translate_button = document.createElement('button');
    translate_button.className = 'btn btn-light';
    translate_button.style.padding = '10px 12px';
    translate_button.innerHTML = 'ترجمة';
    translate_button.type = "button";
    translate_button.id = "Button-gbt2";
    //اضافة لقائمة الخصائص
    targetElement.appendChild(translate_button);

    `""""""""""""الترجمة""""""""""""`
    let iframe = document.getElementsByTagName('iframe')[0]
    let iframeDocument = iframe.contentDocument || iframe.contentWindow.document;
    let iframeBody = iframeDocument.body;
    console.log(iframeBody.innerHTML)
    var myButton = document.getElementById('Button-gbt2');

    // إضافة مستمع للأحداث للنقر على الزر
    myButton.addEventListener('click', function () {
        const apiUrl = 'http://127.0.0.1:5000/app-orign-gbt';
        console.log("ترجم نص الاتش تي ام ال للعربية " + iframeBody.innerHTML)
        // إعداد البيانات التي تريد إرسالها
        const requestData = {
            method: 'POST', // أو 'GET' حسب نوع الطلب
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: "Translate the following page from English to Arabic: " + iframeBody.innerHTML
            }) // بيانات الطلب
        };



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
                iframeBody.innerHTML = data["message"]

            })
            .catch(error => {
                console.error('Error:', error); // التعامل مع الأخطاء
            });
    })
}