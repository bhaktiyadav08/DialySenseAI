const tableBody = document.getElementById("tableBody");
const alertBox = document.getElementById("alert");

const ctx = document.getElementById('chart').getContext('2d');

const chart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: [],
    datasets: [{
      label: 'Temperature',
      data: []
    }]
  }
});

async function fetchData() {
  const res = await fetch("http://127.0.0.1:5000/data");
  const data = await res.json();

  tableBody.innerHTML = "";

  let temps = [];
  let labels = [];

  data.forEach((d, index) => {
    const row = `
      <tr>
        <td>${d.temperature}</td>
        <td>${d.flow_rate}</td>
        <td>${d.water_level}</td>
        <td style="color:${d.status === 'blockage' ? 'red' : 'green'}">
          ${d.status}
        </td>
      </tr>
    `;
    tableBody.innerHTML += row;

    temps.push(d.temperature);
    labels.push(index);
  });

  // Update chart
  chart.data.labels = labels;
  chart.data.datasets[0].data = temps;
  chart.update();

  // ALERT SYSTEM 🚨
  if (data.length > 0 && data[0].status === "blockage") {
    alertBox.innerText = "⚠️ BLOCKAGE DETECTED!";
  } else {
    alertBox.innerText = "";
  }
}

// Auto refresh every 5 sec
setInterval(fetchData, 5000);

// First load
fetchData();