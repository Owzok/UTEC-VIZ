document.addEventListener("DOMContentLoaded", function () {
  (async function () {
    const data = await fetch("/data").then(res => res.json());
    const maxH = Math.max(...data.nodes.map(d => d.h_index || 0));

    function computeTasks(data) {
      return {
        task1: {
          title: "Who are the most prolific collaborators?",
          description: "Faculty with highest degree centrality (most connections)",
          topResults: data.nodes
            .slice()
            .sort((a, b) => b.degree - a.degree)
            .slice(0, 5)
            .map(d => ({
              name: d.name,
              department: d.department,
              degree: d.degree,
              connections: d.degree
            }))
        },
        task2: {
          title: "Which professors act as bridges between departments?",
          description: "Faculty with highest betweenness centrality",
          topResults: data.nodes
            .slice()
            .sort((a, b) => b.betweenness_centrality - a.betweenness_centrality)
            .slice(0, 5)
            .map(d => ({
              name: d.name,
              department: d.department,
              betweenness: d.betweenness_centrality,
              bridge_score: d.betweenness_centrality
            }))
        },
        task3: {
          title: "Who are the most influential faculty members?",
          description: "Faculty with highest combined PageRank and H-index scores",
          topResults: data.nodes
            .slice()
            .map(d => ({
              ...d,
              influence_score: 0.7 * d.pagerank + 0.3 * (d.h_index / maxH)
            }))
            .sort((a, b) => b.influence_score - a.influence_score)
            .slice(0, 5)
            .map(d => ({
              name: d.name,
              department: d.department,
              pagerank: d.pagerank.toFixed(4),
              h_index: d.h_index,
              influence_score: d.influence_score.toFixed(4)
            }))
        },        
        task4: {
          title: "Which departments have the strongest internal collaboration?",
          description: "Departments with highest average clustering coefficient",
          topResults: Object.entries(
            data.nodes.reduce((acc, node) => {
              if (!acc[node.department]) {
                acc[node.department] = { sum: 0, count: 0 };
              }
              acc[node.department].sum += node.clustering;
              acc[node.department].count += 1;
              return acc;
            }, {})
          )
            .map(([dept, info]) => ({
              department: dept,
              avg_clustering: info.sum / info.count,
              faculty_count: info.count,
              internal_collaboration: (info.sum / info.count).toFixed(3)
            }))
            .sort((a, b) => b.avg_clustering - a.avg_clustering)
            .slice(0, 5)
        }
      };
    }

    function renderTaskResults(tasks) {
      const container = d3.select("#task-results");

      container.append("h2")
        .text("Network Analysis Insights")
        .style("font-family", "sans-serif")
        .style("margin-bottom", "20px");

      Object.entries(tasks).forEach(([_, task], index) => {
        const panel = container.append("div")
          .attr("class", "task-panel")
          .style("margin-bottom", "20px");

        const header = panel.append("div")
          .style("cursor", "pointer")
          .style("background", "#2c3e50")
          .style("color", "#fff")
          .style("padding", "10px")
          .style("border-radius", "5px")
          .text(`${index + 1}. ${task.title}`)
          .on("click", function () {
            const body = d3.select(this.nextSibling);
            const isVisible = body.style("display") !== "none";
            body.style("display", isVisible ? "none" : "block");
          });

        const body = panel.append("div")
          .style("display", "none")
          .style("border", "1px solid #ddd")
          .style("padding", "15px")
          .style("border-radius", "0 0 5px 5px")
          .style("background", "#f9f9f9");

        body.append("p")
          .text(task.description)
          .style("font-style", "italic")
          .style("margin-bottom", "10px");

        const table = body.append("table")
          .style("width", "100%")
          .style("border-collapse", "collapse");

        const headers = Object.keys(task.topResults[0] || {});
        const headerRow = table.append("tr");
        headers.forEach(header => {
          headerRow.append("th")
            .text(header.replace(/_/g, " ").toUpperCase())
            .style("padding", "8px")
            .style("border", "1px solid #ddd")
            .style("background", "#f0f0f0")
            .style("text-align", "left");
        });

        task.topResults.forEach((result, i) => {
          const row = table.append("tr")
            .style("background", i % 2 === 0 ? "#fff" : "#f9f9f9");

          headers.forEach(header => {
            row.append("td")
              .text(result[header])
              .style("padding", "8px")
              .style("border", "1px solid #ddd");
          });
        });
      });
    }

    const tasks = computeTasks(data);
    renderTaskResults(tasks);
  })();
});
