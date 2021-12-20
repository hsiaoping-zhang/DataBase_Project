# Songs' Database
資料庫期末 project

## 系統架構與環境
- 使用語言：`python`
- 套件：PyQt5、sqlite3
- 開發環境：Windows 10 + Qt Designer
- 資料庫：`SQLite`

## 介面及使用說明
![](https://i.imgur.com/MeFYoU6.png)

- 目前 TABLE：在執行查詢、刪除時對應的 TABLE
- 選擇方法： SQL指令 / 查詢 / 刪除 / 新增
- column 內容：對於不同的 TABLE 對應其欄位
- 輸入指令：提供使用者輸入
- SELECT / DISTINCT... ：按鈕按下可以直接在指令欄新增按鈕指令
- 執行結果：查看此指令是否成功 (**執行成功後，指令會被清除**)
- 查詢結果：EXISTS 指令的查詢結果
- TABLE 列表：更換主 TABLE (對應 column 內容)
- 大空白框：顯示資料結果處

### SQL 指令使用
不受限於主 TABLE ，可以進行所有 TABLE 操作
```
SELECT * FROM ALBUM WHERE Date < "2010"
```
![](https://i.imgur.com/x0r48na.png)

```SQL=
// INSERT
INSERT INTO ALBUM(album_id, Name) VALUES("AA1", "TESTAA1")

// UPDATE
UPDATE ALBUM SET Date = "test_date" WHERE album_id == "AA1"

// DELETE
DELETE FROM ALBUM WHERE album_id == "AA1"
```

Nested queries

![](https://i.imgur.com/jjN5rxl.png)
```sql=
// IN
SELECT movie_id, Name, Year FROM MOVIE WHERE Year IN (2013, 2014)

// EXISTS
SELECT EXISTS(SELECT 1 FROM MOVIE WHERE Year == 2013)
SELECT EXISTS(SELECT 1 FROM MOVIE WHERE Year == 2021)
```

Aggregate functions

![](https://i.imgur.com/XoFP7L1.png)

```sql=
// COUNT
SELECT COUNT(*) FROM SONG

// SUM
SELECT SUM(Number) FROM CONCERT

// MAX ; MIN
SELECT MAX(Date) FROM ALBUM
SELECT MIN(Date) FROM ALBUM

// AVG
SELECT AVG(Number) FROM SONG

// HAVING
SELECT * FROM CONCERT GROUP BY Series HAVING count(Series) > 20
```

### 按鍵使用
- 流程
    1. 選擇 TABLE 按鍵
    2. 選擇 `查詢`、`刪除`、`新增` 模式
    3. 選擇 column
    4. 使用者輸入
    5. 如有需要，再重複 3~4 步驟
    6. 點選執行
    
如果有成功，就會在旁邊的執行結果顯示；如果失敗，則會顯示錯誤訊息。

**Success**
![](https://i.imgur.com/6ZRFkJm.png)

**Fail**
![](https://i.imgur.com/WcFCexx.png)



## 資料庫設計

- 主題：林俊傑作品資料庫
- 說明：參考維基百科，將林俊傑的歌手專輯、歌曲、演唱會及演出相關影視作品製成此資料庫。
    - [Link](https://zh.wikipedia.org/wiki/%E6%9E%97%E4%BF%8A%E6%9D%B0#%E9%9F%B3%E6%A8%82%E4%BD%9C%E5%93%81)：維基百科
    - [Link](https://zh.wikipedia.org/wiki/%E6%9E%97%E4%BF%8A%E5%82%91%E5%B0%88%E8%BC%AF%E5%88%97%E8%A1%A8)：歌曲列表
- 專案階段流程：
    - 資料蒐集：以網頁爬蟲方式將資料下載，先行存到 csv 檔後進行手動校正
    - 寫入資料庫：以 `python` 將整理完的 csv 檔案寫入 SQLite 資料庫
    - GUI 介面：以 python 搭配套件 `PyQt5` 並使用 `Qt Designer` 進行介面開發，資料庫則是使用 SQLite 進行相關操作

### ER diagram
![](https://i.imgur.com/wtaND9O.png)


- 主打歌：一張專輯一首主打歌，一首歌不一定是主打歌
- 收錄：一張專輯收錄好幾首歌
- 參與：一個音樂電影裡面有歌曲、電影本身和合作對象組合
- 嘉賓：一場演唱會不一定有嘉賓，但一個人可以擔任很多場演唱會嘉賓
- 所在：演唱會可以在同一地方開很多次，但一定要有地方開


### Relation Schema

**SONG** 歌曲
記錄每首歌曲的基本資料

| COLUMN | song_id | album_id | Number | Song |
| :--: | :--: | :--: | :--: | :--: | 
| TYPE | INTEGER | STRING | INTEGER | STRING |

- NO：歌曲編號
- album_id：專輯 ID (連結到 ALBUM table 的 album_id) - 收錄
- Number：專輯曲目編號
- Song：歌曲名稱

<hr/>

**ALBUM** 專輯
記錄專輯的基本資料

| COLUMN | album_id | Name | English | Date | Made | Release | Title |
| :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: |
| TYPE | STRING | STRING | INTEGER | STRING | STRING | STRING | STRING | 

- album_id：專輯代碼
- Name：專輯名稱
- English：專輯英文名稱
- Date：發行日
- Made：製作
- Release：發行
- Title：主打歌 (連結到 SONG table 的 song_id) - 主打歌

<hr/>

**MOVIE** 影視作品
相關的影視如音樂電影 / 音樂愛情故事 的作品及其相關緣自的歌曲

| COLUMN | movie_id | Type | Number | Name | Song | Year | person_id |
| :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: |
| TYPE | STRING | STRING | INTEGER | STRING | STRING | INTGER | STRING |

- movie_id：影視作品編號
- Type：類別
- Number：類型作品編號
- Name：作品名稱
- Song：相關音樂作品 (連結到 SONG table 的 song_id) - 參與
- Year：年份
- Partner：合作者 (連結到 PERSON table 的 person_id) - 參與

<hr/>

**CONCERT** 演唱會
不同系列的巡迴演唱會及嘉賓名單

| COLUMN | concert_id | Series | Number | Date | place_id | person_id |
| :--: | :--: | :--: | :--: | :--: | :--: | :--: |
| TYPE | STRING | STRING | INTEGER | STRING | STRING | STRING |

- concert_id：演唱會編號
- Series：演唱會系列
- Number：系列場次
- Date：演唱會日期
- place_id：地點代碼 (連結到 PLACE table 的 place_id) - 所在
- person_id：嘉賓代碼 (連結到 PERSON table 的 person_id) - 嘉賓

<hr/>

**PLACE** 地點
舉辦演唱會的地點資訊

| COLUMN | place_id | Country | City | Place | 
| :--: | :--: | :--: | :--: | :--: |
| TYPE | STRING  | STRING | STRING | STRING | 

- place_id：場地編號
- Country：國家
- City：城市
- Place：場館名稱

<hr/>

**PERSON** 嘉賓名單
合作對象的基本資料

| COLUMN | person_id | Name | Sex |
| :--: | :--: | :--: | :--: |
| TYPE | STRING | STRING | STRING | 

- person_id：人物編號
- Name：名字
- Sex：性別
