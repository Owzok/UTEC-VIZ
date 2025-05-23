(async function() {
    const rawData = await fetch('/data').then(res => res.json());
  
    const nodes = rawData.nodes.map(d => ({
      ...d,
      id: d.id,
      x: Math.random() * 800,
      y: Math.random() * 600
    }));
  
    const links = rawData.edges.map(d => ({
      ...d,
      source: d.source,
      target: d.target
    }));
  
    const data = {
      nodes,
      links,
      departments: rawData.departments,
      department_colors: rawData.department_colors,
      stats: rawData.stats
    };
  
    const width = 1920;
    const height = 500;
  

    const stats = {
      totalNodes: data.nodes.length,
      totalLinks: data.links.length,
      totalDepartments: data.departments.length,
      avgDegree: d3.mean(data.nodes, d => d.degree).toFixed(2),
      networkDensity: (2 * data.links.length / (data.nodes.length * (data.nodes.length - 1))).toFixed(4),
      avgClustering: d3.mean(data.nodes, d => d.clustering).toFixed(3)
    };
  
    const statsContainer = d3.select("#stats")
      .append("div")
      .style("margin", "20px 0");
  
    statsContainer.append("h3")
      .text("Network Statistics")
      .style("color", "#2c3e50");
  
    const statsGrid = statsContainer.append("div")
      .style("display", "grid")
      .style("grid-template-columns", "repeat(auto-fit, minmax(200px, 1fr))")
      .style("gap", "15px")
      .style("margin-top", "15px");
  
    Object.entries(stats).forEach(([key, value]) => {
      const statBox = statsGrid.append("div")
        .style("padding", "15px")
        .style("border", "1px solid #ddd")
        .style("border-radius", "5px")
        .style("background", "#f8f9fa")
        .style("text-align", "center");
  
      statBox.append("div")
        .text(value)
        .style("font-size", "24px")
        .style("font-weight", "bold")
        .style("color", "#2980b9");
  
      statBox.append("div")
        .text(key.replace(/([A-Z])/g, " $1").trim())
        .style("font-size", "12px")
        .style("color", "#666")
        .style("margin-top", "5px");
    });
  
    const svg = d3.select("#chart")
      .append("svg")
      .attr("width", "100%")
      .attr("height", height)
      .style("background", "#fafafa");
  
    const g = svg.append("g");
  
    const zoom = d3.zoom()
      .scaleExtent([0.1, 5])
      .on("zoom", (event) => {
        g.attr("transform", event.transform);
      });
  
    svg.call(zoom);
  
    const simulation = d3.forceSimulation(data.nodes)
      .force("link", d3.forceLink(data.links).id(d => d.id).distance(50).strength(0.5))
      .force("charge", d3.forceManyBody().strength(-1500))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("x", d3.forceX(width / 2).strength(0.1))
      .force("y", d3.forceY(height / 2).strength(0.1))
      .force("collision", d3.forceCollide().radius(d => d.size + 5))
      .on("tick", ticked);
  
    const link = g.append("g")
      .selectAll("line")
      .data(data.links)
      .enter().append("line")
      .attr("stroke", "#999")
      .attr("stroke-opacity", d => Math.min(1, d.weight))
      .attr("stroke-width", d => Math.sqrt(d.weight) * 2);
  
    const node = g.append("g")
      .selectAll("g")
      .data(data.nodes)
      .enter().append("g")
      .call(d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended));
  
    node.append("circle")
      .attr("r", d => d.size)
      .attr("fill", d => d.color || "#69b3a2")
      .attr("stroke", "#fff")
      .attr("stroke-width", 2);
  
    node.filter(d => d.image_url)
      .append("image")
      .attr("xlink:href", d => d.image_url)
      .attr("x", d => -d.size * 0.8)
      .attr("y", d => -d.size * 0.8)
      .attr("width", d => d.size * 1.6)
      .attr("height", d => d.size * 1.6)
      .attr("clip-path", "circle()");
  
    node.append("text")
      .text(d => d.name.split(" ").slice(-2).join(" "))
      .attr("x", 0)
      .attr("y", d => d.size + 15)
      .attr("text-anchor", "middle")
      .attr("font-size", "10px")
      .attr("fill", "#333");
  
    node.append("title")
      .text(d => `${d.name}\nDepartment: ${d.department}\nH-index: ${d.h_index}\nCitations: ${d.citations}`);
  
    const legend = svg.append("g")
      .attr("class", "legend")
      .attr("transform", `translate(${width - 550}, 50)`);

    const legendItems = legend.selectAll(".legend-item")
      .data(data.departments)
      .enter().append("g")
      .attr("class", "legend-item")
      .attr("transform", (d, i) => `translate(0, ${i * 25})`);

    legendItems.append("circle")
      .attr("r", 8)
      .attr("fill", d => data.department_colors[d]);
    
    legendItems.append("text")
      .attr("x", 15)
      .attr("y", 5)
      .text(d => d.replace("Departamento de ", ""))
      .attr("font-size", "12px")
      .attr("font-family", "Arial, sans-serif");


    function ticked() {
      link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);
  
      node.attr("transform", d => `translate(${d.x},${d.y})`);
    }
  
    function dragstarted(event, d) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }
  
    function dragged(event, d) {
      d.fx = event.x;
      d.fy = event.y;
    }
  
    function dragended(event, d) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }
  })();  