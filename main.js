const weightClasses = {
  "Women's Strawweight": -1,
  "Flyweight": 1,
  "Women's Flyweight": 0,
  "Bantamweight": 3,
  "Women's Bantamweight": 2,
  "Featherweight": 5,
  "Women's Featherweight": 4,
  "Lightweight": 7,
  "Women's Lightweight": 6,
  "Welterweight": 9,
  "Women's Welterweight": 9,
  "Middleweight": 10,
  "Women's Middleweight": 11,
  "Light Heavyweight": 12,
  "Heavyweight": 15
};
// Select the fighters list table
const fightersTable = document.querySelector('table');

// Retrieve the CSV file using fetch()
fetch('https://raw.githubusercontent.com/JosPerez/MMABoard.github.io/main/fighters.csv')
  .then(response => response.text())
  .then(data => {
    // Use the csv-parse library to parse the CSV data
    const fighters = Papa.parse(data, { header: true });

    // Sort the fighters by their record in descending order
    fighters.data.sort((a, b) => {
      const recordA = a.Record.split('(')[0].trim().split('-');
      const recordB = b.Record.split('(')[0].trim().split('-');
      const winsA = parseInt(recordA[0]);
      const winsB = parseInt(recordB[0]);
      if (winsA > winsB) {
        return -1;
      } else if (winsA < winsB) {
        return 1;
      } else {
        return 0;
      }
    });

    // Get the top 8 fighters
    const topFighters = fighters.data.slice(0, 9);

    // Create an HTML list of the top fighters
    const topFightersList = document.createElement('ul');
    topFightersList.classList.add('card-list');
    topFighters.forEach(fighter => {
      const listItem = document.createElement('li');
      listItem.classList.add('card');
      const title = document.createElement('h2');
      const summary = document.createElement('p');

      title.textContent = fighter.Name;
      summary.textContent = fighter.Record;

      listItem.appendChild(title);
      listItem.appendChild(summary);
      topFightersList.appendChild(listItem);
    });

    // Add the HTML list to the page
    const newsSection = document.querySelector('.news');
    newsSection.appendChild(topFightersList);


    // Loop through the rows and create the table rows
    fighters.data.forEach((row) => {
      const tableRow = document.createElement('tr');
      tableRow.innerHTML = `
        <td>${row['Name']}</td>
        <td>${row['Weight Class']} </td>
        <td>${row['Record']}</td>
      `;
      fightersTable.querySelector('tbody').appendChild(tableRow);
    });

    createFighterList(fighters.data.slice(30, 40),fighters.data.slice(100, 110));
  })
  .catch(error => console.error(error));

  function sortTable(table, column, asc = true) {
    const tbody = table.querySelector("tbody");
    const rows = Array.from(tbody.querySelectorAll("tr"));

    if (column === 1) {
      rows.sort((a, b) => {
        const aWeightClass = weightClasses[a.querySelector(`td:nth-child(${column + 1})`).innerText.trim()];
        const bWeightClass = weightClasses[b.querySelector(`td:nth-child(${column + 1})`).innerText.trim()];
        
        if (aWeightClass < bWeightClass) {
          return -1;
        } else if (aWeightClass > bWeightClass) {
          return 1;
        } else {
          return 0;
        }
      });
    } else if (column === 2) {
      rows.sort((row1, row2) => {
        const cellValue1 = row1.querySelector(`td:nth-child(${column + 1})`).innerText.trim();
        const cellValue2 = row2.querySelector(`td:nth-child(${column + 1})`).innerText.trim();
        const winsA = parseInt(cellValue1.split("-")[0]);
        const winsB = parseInt(cellValue2.split("-")[0]);
        
        if (winsA > winsB) {
          return -1;
        } else if (winsA < winsB) {
          return 1;
        } else {
          return 0;
        }
      });
    } else { 
      // Sort rows based on column value
      rows.sort((row1, row2) => {
        const cellValue1 = row1.querySelector(`td:nth-child(${column + 1})`).innerText.trim();
        const cellValue2 = row2.querySelector(`td:nth-child(${column + 1})`).innerText.trim();
        return asc ? cellValue1.localeCompare(cellValue2) : cellValue2.localeCompare(cellValue1);
      });
    }
  
    // Reorder table rows based on the sorted rows
    rows.forEach((row) => tbody.appendChild(row));
  }
  
  const table = document.querySelector("table");
  const headers = table.querySelectorAll("th");
  
  headers.forEach((header, i) => {
    header.addEventListener("click", () => {
      // Determine the current sort order and toggle it
      const ascending = header.getAttribute("data-order") === "asc";
      header.setAttribute("data-order", ascending ? "desc" : "asc");
  
      // Sort the table by the selected column and order
      sortTable(table, i, ascending);
    });
  });
  function createFighterList(add, remove) {
    // Get the fighter list container element
    const addFighterList = document.querySelector('#added');
    const removeFighterList = document.querySelector('#removed');
    // Add each fighter to the list
    add.forEach((fighter) => {
      const fighterItem = document.createElement('li');
      fighterItem.classList.add('fighter-list__item');
      fighterItem.textContent = fighter['Name'] + " " +  fighter['Record'];
      addFighterList.appendChild(fighterItem);
    });
    // Add each fighter to the list
    remove.forEach((fighter) => {
      const fighterItem = document.createElement('li');
      fighterItem.classList.add('fighter-list__item');
      fighterItem.textContent = fighter['Name'] + " " +  fighter['Record'];
      removeFighterList.appendChild(fighterItem);
    });
  }