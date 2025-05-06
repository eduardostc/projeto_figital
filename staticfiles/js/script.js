document.addEventListener("DOMContentLoaded", function() {
    var phoneInputs = document.querySelectorAll(".mask-telefone");
    phoneInputs.forEach(function(input) {
        input.addEventListener("input", function() {
            let value = input.value.replace(/\D/g, '');
            if (value.length <= 10) {
                input.value = value.replace(/^(\d{2})(\d{4})(\d{0,4})$/, "($1) $2-$3");
            } else {
                input.value = value.replace(/^(\d{2})(\d{5})(\d{0,4})$/, "($1) $2-$3");
            }
        });
    });
});
