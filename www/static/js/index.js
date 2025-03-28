function onDragStart(event) {
  console.log(event);
  event.dataTransfer.setData("dragged-card-id", event.target.id);
}

function onDragOver(event) {
  event.preventDefault();
}

function onDrop(event) {
  console.log(event);
  event.preventDefault();
  const data = event.dataTransfer.getData("dragged-card-id");
  event.target.appendChild(document.getElementById(data));
}
