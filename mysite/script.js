fetch("https://restcountries.com/v3.1/all")
  .then((res) => res.json())
  .then((data) => {
    console.log("Fetched countries data:", data);
    const datalist = document.getElementById("countries");

    if (datalist) {
      const sortedCountries = data.sort((a, b) =>
        a.name.common.localeCompare(b.name.common)
      );

      datalist.innerHTML = "";
      sortedCountries.forEach((country) => {
        const option = document.createElement("option");
        option.value = country.name.common;
        datalist.appendChild(option);
      });
    }
  })
  .catch((error) => {
    console.error("Error fetching country data:", error);
  });
