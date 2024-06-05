window.addEventListener("DOMContentLoaded", () => {
 const websocket = new WebSocket("ws://192.29.5.20:6788/");


 document.querySelector(".minus").addEventListener("click", () => {
   websocket.send(JSON.stringify({ action: "minus" }));
 });


 document.querySelector(".plus").addEventListener("click", () => {
   websocket.send(JSON.stringify({ action: "plus" }));
 });


 websocket.onmessage = ({ data }) => {
   const event = JSON.parse(data);
   switch (event.type) {
     case "value2":
       document.querySelector(".value2").textContent = event.value2;
       break;
     case "value1":
       document.querySelector(".value1").textContent = event.value1;
       break;
     case "users":
       const users = `${event.count} User${event.count == 1 ? "" : "s"}`;
       // const users = `${event.count}`;
       document.querySelector(".users").textContent = users;
       break;
     default:
       console.error("unsupported event", event);
   }
 };
});
