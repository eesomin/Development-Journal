const { app, BrowserWindow } = require("electron");
const path = require("path");

// 전역변수 설정
let mainWindow

function createWindow (){
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600
    })

    // index.html 불러오기
    mainWindow.loadFile(path.join(__dirname, "index.html"));

}

// 창 나타내기
app.whenReady().then(createWindow);

// 모든 창이 닫히면 앱 종료
app.on("window-all-closed", () => {
    if (process.platform !== "darwin") {
        app.quit();
    }
});
