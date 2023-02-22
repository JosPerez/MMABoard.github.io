function googleTranslateElementInit() {
  new google.translate.TranslateElement({pageLanguage: 'en'}, 'google_translate_element');
}

// Call the googleTranslateElementInit function after the page has finished loading
window.onload = function() {
  googleTranslateElementInit();
};
const weightClasses = {
  "Women's Strawweight": 0,
  "Flyweight": 2,
  "Women's Flyweight": 1,
  "Bantamweight": 4,
  "Women's Bantamweight": 3,
  "Featherweight": 6,
  "Women's Featherweight": 5,
  "Lightweight": 8,
  "Women's Lightweight": 7,
  "Welterweight": 10,
  "Women's Welterweight": 9,
  "Middleweight": 12,
  "Women's Middleweight": 11,
  "Light Heavyweight": 13,
  "Heavyweight": 14
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
    const cleanFighters = fighters.data.filter(item => item['Name'] !== '');
    cleanFighters.sort((a, b) => {
      const recordA = a.Record.split('(')[0].trim().split('-');
      const recordB = b.Record.split('(')[0].trim().split('-');
      const winsA = parseInt(recordA[0]);
      const winsB = parseInt(recordB[0]);
      if (winsA > winsB) {
        return -1;
      } else if (winsA < winsB) {
        return 1;
      }
      return 0;
    });
    const undefeatedFighter = cleanFighters.filter(item => parseInt(item['Record'].split("-")[1]) === 0);
    console.log(undefeatedFighter)
    // Get the top 8 fighters
    const topFighters = undefeatedFighter.slice(0, 12);

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
    cleanFighters.forEach((row) => {
      const tableRow = document.createElement('tr');
      tableRow.innerHTML = `
        <td>${row['Name']}</td>
        <td>${row['Weight Class']} </td>
        <td>${row['Record']}</td>
      `;
      fightersTable.querySelector('tbody').appendChild(tableRow);
    });
  })
  .catch(error => console.error(error));
// Retrieve the CSV file using fetch()
fetch('https://raw.githubusercontent.com/JosPerez/MMABoard.github.io/main/ufc_events.csv')
.then(response => response.text())
.then(data => {
  // Use the csv-parse library to parse the CSV data
  const fighters = Papa.parse(data, { header: true });
  // Get the fighter list container element
  const removeFighterList = document.querySelector('.carousel');
  const fights = fighters.data.filter(item => item['Event'] !== '');
  fights.forEach((fighter) => {
    const fighterItem = document.createElement('li');
    const title = document.createElement('h3');
    title.textContent = fighter['Event'];
    title.classList.add('event-title')
    const date = document.createElement('p');
    date.classList.add('event-date-time')
    date.textContent = fighter['Date']
    const place = document.createElement('p');
    place.classList.add('event-date-time')
    place.textContent = fighter['Place']
    fighterItem.appendChild(title)
    fighterItem.appendChild(date)
    fighterItem.appendChild(place)
    removeFighterList.appendChild(fighterItem);
  });
})
.catch(error => console.error(error));
  // Retrieve the CSV file using fetch()
fetch('https://raw.githubusercontent.com/JosPerez/MMABoard.github.io/main/fighters_added.csv')
.then(response => response.text())
.then(data => {
  // Use the csv-parse library to parse the CSV data
  const fighters = Papa.parse(data, { header: true });
  createFighterListAdd(fighters.data)
})
.catch(error => console.error(error));
  // Retrieve the CSV file using fetch()
  fetch('https://raw.githubusercontent.com/JosPerez/MMABoard.github.io/main/fighters_removed.csv')
  .then(response => response.text())
  .then(data => {
    // Use the csv-parse library to parse the CSV data
    const fighters = Papa.parse(data, { header: true });
    createFighterListRemove(fighters.data);
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
          return asc ? -1 : 1;
        } else if (aWeightClass > bWeightClass) {
          return asc ? 1 : -1;
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
        const losesA = parseInt(cellValue1.split("-")[1]);
        const losesB = parseInt(cellValue2.split("-")[1])
        const diffA = winsA - losesA;
        const diffB = winsB - losesB;
        
        // Compare the number of wins
        if (winsA > winsB) {
          return asc ? -1 : 1;
        } else if (winsA < winsB) {
          return asc ? 1 : -1;
        } else {
          // If the number of wins is the same, compare the number of losses
          if (losesA < losesB) {
            return asc ? -1 : 1;
          } else if (losesA > losesB) {
            return asc? 1 : -1;
          } else {
            if (diffA > diffB) {
              return asc ? -1 : 1;
            } else if (diffA < diffB) {
              return asc ? 1 : -1;
            } else {
              return 0;
            }
          }
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
  function createFighterListAdd(add) {
    // Get the fighter list container element
    const addFighterList = document.querySelector('#added');
    add = add.filter(item => item['Name'] !== '');
    // Add each fighter to the list
    add.forEach((fighter) => {
      const fighterItem = document.createElement('li');
      fighterItem.classList.add('fighter-list__item');
      fighterItem.textContent = fighter['Name'] + " " +  fighter['Record'];
      addFighterList.appendChild(fighterItem);
    });
  }
  function createFighterListRemove(remove) {
    // Get the fighter list container element
    const removeFighterList = document.querySelector('#removed');
    remove = remove.filter(item => item['Name'] !== '');
    remove.forEach((fighter) => {
      const fighterItem = document.createElement('li');
      fighterItem.classList.add('fighter-list__item');
      fighterItem.textContent = fighter['Name'] + " " +  fighter['Record'];
      removeFighterList.appendChild(fighterItem);
    });
  }
