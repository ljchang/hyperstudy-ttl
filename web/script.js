let device;

document.getElementById("connect").onclick = async () => {
  try {
    device = await navigator.usb.requestDevice({ filters: [{ vendorId: 0x239A }] });
    await device.open();
    await device.selectConfiguration(1);
    await device.claimInterface(0);
    log("✅ Connected to device");
    document.getElementById("pulse").disabled = false;
  } catch (err) {
    log("❌ " + err);
  }
};

document.getElementById("pulse").onclick = async () => {
  if (!device) return;
  const encoder = new TextEncoder();
  const data = encoder.encode("pulse\n");
  await device.transferOut(1, data);
  log("⚡ Sent pulse command");
};

function log(msg) {
  document.getElementById("log").textContent += msg + "\n";
}
