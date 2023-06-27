selectCommercialUse = document.getElementsByName("commercial_use")[0]

// Disable company name input if commercial use is false
selectCommercialUse.addEventListener("change", (event) => {
    document.getElementsByName("company_name")[0].disabled = event.target.value != "True"

})