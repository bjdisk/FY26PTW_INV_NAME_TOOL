# 邀請函姓名工具

純前端單頁工具，給銷售顧問使用。顧問只輸入客戶姓名並選擇稱謂，預覽確認後存成 1080×2348 的 JPG（iPhone 18 Pro 全螢幕比例）。iPhone 會跳出分享選單，點「儲存影像」就存進相簿；Android 會存到相簿的 Download 資料夾。
字型、字級、顏色、位置都鎖在 `config/ci.json`，只有開發者能改。

## 檔案
- `index.html`：網站首頁，由 `sh build.sh` 從 `src/app.html` 產生。
- `config/ci.json`：正式 CI 設定。開發者面板按「發佈給所有顧問」會直接改寫這個檔案。
- `fonts/`：Porsche Next Regular、華康中黑體(P)／粗黑體(P)。華康已修復 cmap，並切成約 500 字一包（`fonts/DFHeiMediumP/`），網頁只下載姓名用到的那幾包。`coverage.txt` 用來偵測罕用字。
- `template/`：正式底圖，開發者面板發佈時會自動上傳到這裡。
- `tools/fixfont.py`：把華康 TTC 修成瀏覽器可用的 woff2。
- `tools/split_fonts.py`：把 woff2 切成小包並產生 manifest.json。

## 上線（GitHub Pages）
repo 的 Settings → Pages → Build and deployment 選 **Deploy from a branch**，Branch 選 `main`、資料夾選 `/ (root)`，然後按 Save。
約 1 分鐘後網址會顯示在同一頁，格式是 `https://bjdisk.github.io/FY26PTW_INV_NAME_TOOL/`。
注意：這個網址是公開的，只要知道網址就能開啟，請只發給內部人員。

### 用 LINE 傳連結
LINE 內建瀏覽器無法下載圖片。傳連結時請在網址後面加上 `?openExternalBrowser=1`，LINE 就會直接用手機的 Chrome／Safari 開啟：
`https://bjdisk.github.io/FY26PTW_INV_NAME_TOOL/?openExternalBrowser=1`
若顧問還是在 LINE 裡打開，頁面頂端也會提示改用瀏覽器開啟。

## 開發者面板
1. 點畫面左上角的小齒輪，輸入開發者密碼。
2. 調整字型、字級、位置、顏色，或更換底圖（建議 1080×2348 直式，其他尺寸會自動置中裁切）。可以直接在預覽圖上拖曳位置，預覽會即時更新，但只有你看得到。
3. 按「發佈給所有顧問」。第一次使用要貼上 GitHub 權杖，權杖只會存在這台電腦的瀏覽器裡。
4. GitHub 約 1～2 分鐘後更新網站，顧問重新整理頁面就會套用新設定。

### 產生 GitHub 權杖（只要做一次）
GitHub → Settings → Developer settings → Personal access tokens → **Fine-grained tokens** → Generate new token：
- Repository access：Only select repositories → `FY26PTW_INV_NAME_TOOL`
- Permissions → Repository permissions → **Contents：Read and write**
- 其他權限都不用開。

## 本機試用
在此資料夾執行 `python3 -m http.server`，開 http://localhost:8000 。直接雙擊 index.html 會讀不到字型與設定檔。

## 授權
Porsche Next、華康字型皆為商用字型，僅供內部人員使用。
