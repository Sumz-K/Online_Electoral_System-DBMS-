const inputs = document.getElementById("inputs");

inputs.addEventListener("input", function (e) {
    const target = e.target;
    const val = target.value;
    if (isNaN(val)) {
        target.value = "";
        return;
    }

    if (val != "") {
        const next = target.nextElementSibling;
        if (next) {
            next.focus();
        }
        else{
            document.activeElement.blur()
            
            button1 = document.getElementById("bid")
            button1.disabled = false
            button1.style.backgroundColor="#32a854"
            document.getElementById("myForm").submit();

        }
    }
});

inputs.addEventListener("keyup", function (e) {
    const target = e.target;
    const key = e.key.toLowerCase();
    if (key == "backspace" || key == "delete") {
        console.log(target.value);
        if (target.value == "") {
            const prev = target.previousElementSibling;
            if (prev) {
                prev.value = ""
                prev.focus();
            }

        }
        else{
            target.value = "";
            target.focus()
        }
        
        return;
    }
});