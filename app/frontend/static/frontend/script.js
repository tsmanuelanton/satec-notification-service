radioBtnYes = document.getElementsByName("commercial_use")[0]
radioBtnNo = document.getElementsByName("commercial_use")[1]

// Disable company name input if commercial use is false
radioBtnYes.addEventListener("change", (event) => {
    isForCommercialUse = event.target.value == "True"
    setDisabledCompanyNameInput(isForCommercialUse)
})

radioBtnNo.addEventListener("change", (event) => {
    isForCommercialUse = event.target.value == "True"
    setDisabledCompanyNameInput(isForCommercialUse)
})

const setDisabledCompanyNameInput = (isForCommercialUse) => {
    inputCompanyName = document.getElementsByName("company_name")[0]
    if (isForCommercialUse) {
        inputCompanyName.disabled = false
    }else {
        inputCompanyName.disabled = true
        inputCompanyName.value = ""
    }
}