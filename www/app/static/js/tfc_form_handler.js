import { confetti } from './confetti.min.js';

const start = () => {
    setTimeout(function () {
        confetti.start()
    }, 100); // 1000 is time that after 1 second start the confetti ( 1000 = 1 sec)
};

//  Stop

const stop = () => {
    setTimeout(function () {
        confetti.stop()
    }, 1000); // 5000 is time that after 5 second stop the confetti ( 5000 = 5 sec)
};

const onBlur = (e) => {
    if (e.target.value === '') {
        e.target.value = e.target.defaultValue;
    }
}

const onFocus = (e) => {
    e.target.value = '';
}

async function getFormStatus(form_name) {
    const stat_url = `/get_form_status?form_name=${form_name}`
    const response = await fetch(stat_url);
    const jsonbody = await response.json();
    return jsonbody
}

window.onload = function () {
    const tfc_form = document.getElementById("tfc-form");
    const input_divs = [].slice.call(tfc_form.querySelectorAll('input[type="text"]'));

    input_divs.forEach(element => {
        element.addEventListener('focus', onFocus);
        element.addEventListener('blur', onBlur);
    });

    tfc_form.addEventListener('submit', () => {
        localStorage.do_TFC_Confetti = 'true';
    });

    getFormStatus('tfc_form').then(jsonbody => {
        const form_status = jsonbody["ready"];
        const doConfetti = localStorage.do_TFC_Confetti

        // if (form_status) {
        // // tfc_form_display.removeChild(tfc_form);
        // tfc_form_results.style.display = "block";

        if (form_status && doConfetti === 'true') {
            start();
            stop();
            localStorage.do_TFC_Confetti = 'false'
        }

        // }
    });

}

