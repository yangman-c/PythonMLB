import EastMoneyController
import sys
import openpyxl
import common.globalConfig

cookie1 = 'qgqp_b_id=3815b4a4d87774a2e3ccb5c584ae133e; st_si=08039223976786; p_origin=http%3A%2F%2Fpassport2.eastmoney.com; ct=OfKOBzxLyUwUgTZKBn2OVBknkWRf59rzZeYr9QL8AlpZfNf_PS5ytDxJvz8rO2khwpb_SRoOOTJ9ROH2IwYxZry7BnmCwBK506c0cvQEZphxtgIskI_DOAde-LjcQXWHJzP5_I3PKtimRmavqLu7j7t0fx86iRF8i4l19l8ouAw; ut=FobyicMgeV49XUj9B_m01evqF4A4hiLnvP2qQeO0nI1J_30JWSqygD3tQf199fVaYG-89_P5WGwB7mkIAOJLB2bDsuD8ct8eT_rpwoBgSLibtDpdcCp94y3m7_E19li0AqsQltL2KSXihiHsH2phP549BTMX1SJnwD27byPb81UMXZNdw5F5GH8KtvlsI-cr5Ru3U58yZRTmvd90M_2ChailhqusZ9BnPgQe8RRyU8YQEiJROjxWk2SClWdz6PwHxZODXA2eI2ZBQOdpxdpK29vpyOjKZj1v; pi=7723166100673646%3bb7723166100673646%3b%e8%82%a1%e5%8f%8b0761W5651a%3bkulFa6bHv%2bkCAnGRL%2fqaNI0pwXzRUhnqU1k9ADrkL5lJwiEksbVxLoppaa%2bAUt77Xug80ePUj6mRxsob0ZFzEQQpA2o5xOqQGsbl9UXLRALLPROMkdAS81bjHMS2Ev%2f%2fVTsaQgfghhtTPZbYhXuUa1cyXH5InweMGTOgr%2fuCkgOjsDmIn9helIpjFQU02XpTyHbfn6od%3bq7YjmOXArmdSeJmEPpt%2bM5Ia9ko0BJuzHYcmlINFap7OXbVOI4YjimAsVnW9MXIWksnUeG%2fYOxDe%2bz0A4mCTansyfKKhlZkUypWQnnpzRPk04QMz43eJYsL7kFTKa2oxDrQvXOjv%2bDJDUswEfxONife1%2bFej%2bQ%3d%3d; uidal=7723166100673646%e8%82%a1%e5%8f%8b0761W5651a; sid=136059598; vtpst=|; st_pvi=03185002285832; st_sp=2021-02-04%2022%3A32%3A58; st_inirUrl=http%3A%2F%2Fpassport2.eastmoney.com%2F; st_sn=2; st_psi=20210204223332555-113200301712-2853517140; st_asi=20210204223332555-113200301712-2853517140-Web_so_ss-2'

cookie2 = 'st_si=62877598833088; em_hq_fls=js; st_asi=delete; qgqp_b_id=1552060ec5afc5fc10a3e51e88ec7671; waptgshowtime=202125; p_origin=https%3A%2F%2Fpassport2.eastmoney.com; ct=gajxsi-0tBp-dyJbg5VCBb-dhNg3ZybF2dUl5jdObjE8Nza43LkhNtRHhu2QsMSAhmu0wVh7icGZ4wvLJ6uGlRs1r-01_6UExdzYKSS939uMo01OMQV-ExvcTWIg9eBrEDq366zWRqdQBIDsjdP8GM2n9KJNMj7yLfQtXx3t91I; ut=FobyicMgeV7CWBTmL9Bu1qAvtG39cfeJRs5waHsNI8_6xiDrnriWCgyy3Vy13nxxpKJYZjRfLN63WJL3jMd2A_oN1jj7u2S9DrKUvhNJSF_YU3LdhGRKwOLEVgkhnhoA1aFEcNZtziSPloChHdWws3LPZEUI0CfM5rxORIZQSD4H91-AlUxxj3MZR_D8pLVisGVmsH4-dxjl7zXmKebmFSuT2yeTjKk2-gD1YeXZ8ixwL_UPQx7SkIwrVCOZ5aAhAkJJ23b6hAe7yqjX0UgohGBuC72D5xjw; pi=7531336125345560%3bg7531336125345560%3b%e8%82%a1%e5%8f%8bJT89560809%3b2xRrbSVAtUju7mPvj71Ctojh59MoDkG2ANjECOU7nf2SRvJOhaZcCHoKiA7BqQSfO7Yyk2lGGZ2zaS9t8QoO8GQM15YVh4jXOgMOr8PIRD27dgoHYU5tU%2b8VjLtCpnpVCdUtFq2mOXfORoZ2B%2fz5YiM4nS8BqIEfBWjpw2BLkFWFeZsuG8pLyR9H0CyOG84RiY3%2b%2fxFR%3bd5vYnXAh6C4ErO6NQK%2b3O54Qc2Gj32yLo0FbE1iEG57tWcnTfrr61rKSBwMT8EXsMrONJBNp%2fLlqVAeXrD%2fiN1cuce%2fAMCAd9Qsfvysg1aIwT3uXXVw2wbcbuDXlJ6orh20Xp4ihlrr8QHmMiTypjjf7u1kE7w%3d%3d; uidal=7531336125345560%e8%82%a1%e5%8f%8bJT89560809; sid=159709538; vtpst=|; HAList=a-sz-300059-%u4E1C%u65B9%u8D22%u5BCC%2Ca-sh-605358-%u7ACB%u6602%u5FAE%2Ca-sh-601100-%u6052%u7ACB%u6DB2%u538B; st_pvi=30807754692527; st_sp=2019-04-10%2022%3A48%3A30; st_inirUrl=https%3A%2F%2Fwww.baidu.com%2Flink; st_sn=35; st_psi=20210205221658435-113200301712-6509908292'

cookie_dlp = 'st_si=62877598833088; em_hq_fls=js; qgqp_b_id=1552060ec5afc5fc10a3e51e88ec7671; p_origin=https%3A%2F%2Fpassport2.eastmoney.com; sid=159709538; vtpst=|; HAList=a-sz-300059-%u4E1C%u65B9%u8D22%u5BCC%2Ca-sh-605358-%u7ACB%u6602%u5FAE%2Ca-sh-601100-%u6052%u7ACB%u6DB2%u538B; waptgshowtime=2021217; ct=NaNeulFFH78e17okeL2LudsFzNAikAQvoOnyqpz10VHe5C4VZK3BFqqWPnmLe-bQdbA_laBeKuJmyAVLz_SDU32mCRuyHrWP1pQzps8yyHwEicA_Lwo5Tm_fJQg8Eb-tW72UsfYS279fDsKr7LoTyd8PQ4l79gMQflJbBg4Y9os; ut=FobyicMgeV49XUj9B_m01evqF4A4hiLn5hB_RITiOTddxtGj97nwpOKKK6tegZ0z9YYGsj7dOim6rITf7pYOGbtxseR6w9ElNqFVY7_DdUoMpmvP-ugVQ-IozlQ4B61w-mSL-4rcwfeNIPGNNx3gQaCWWxCQTqbzctn5IcS8UHhUEEKJ9SVm4Dp0jqk4Rqd7SOgcT4hoO9On5c0nA5h9fscyGRXrXSokbwb48677u1obF7_zRgQk81KZ5XEcg7Qkyfpqd_wB8spSkPL5vBWQbGSVkFyDeEZj; pi=4234306135506856%3bu4234306135506856%3b%e8%82%a1%e5%8f%8bS212P32705%3benIyvUHcXM2HY6jUpJNWNB%2fxmMMG00sdUQfPA5k7R2EY7h6YQgOVXs3Qphh4L6RbZCVmRkM8RDlil42VFmPpxERN2OTDQp8rQzeSQthVTe6tFG%2fusps%2b9imM1o%2bOQO8mP5UQFz%2fqC4oOCZUs57S%2bz6aPvcfnZCE5oRE%2frSjL0E7T27dFFCXJPRIkr65jZBS0JU3vxrNz%3bw4GybGT5BlFQbX2IWml6vTUrl4xhozu874wXMI0w43P%2bt0SLhi5GzjtV2hD4VDQ4YH9h0lpTggBX6q7SXJjcgwAtlNxFeZ2taqW8lKEF5dWYgYutW6cfrFXJWgr4y6IAbeyXUj1LBxPIJ8y3ykI46eXOdVmBvA%3d%3d; uidal=4234306135506856%e8%82%a1%e5%8f%8bS212P32705; st_asi=delete; st_pvi=30807754692527; st_sp=2019-04-10%2022%3A48%3A30; st_inirUrl=https%3A%2F%2Fwww.baidu.com%2Flink; st_sn=56; st_psi=20210217163202895-113200301712-3917066540'

allCooies = (cookie1, cookie2, cookie_dlp)
def addInteresting(readFile, recordLine, newGroup):
    print(f"readFile:{readFile} recordLine:{recordLine} newGroup:{newGroup}")
    try:
        wb = openpyxl.open(readFile)
    except Exception as err:
        print(err)
        sys.exit()

    ctls = []
    for cookie in allCooies:
        ctl = EastMoneyController.EastMoneyController(cookie)
        ctls.append(ctl)
        if newGroup == "y":
            groupName = readFile[readFile.index("Ranking_") + len("Ranking_"):]
            groupName = groupName.replace(".xlsx", "").replace("-", "")
            ctl.checkAndCreateNewGroup(groupName)

    for row in wb.active.rows:
        code = row[0].value
        # 删除第一行
        if code == "Code":
            continue
        if code in common.globalConfig.blackList:
            continue
        record = 0
        for j in range(1,len(list(row)) - 1):
            if row[j].value == 1:
                record += 1

        if record >= int(recordLine):
            for ctl in ctls:
                ctl.addNewCode(code)

    print("addInteresting ok")

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("参数必须是3个")
        sys.exit()
    readFile = sys.argv[1]
    # 目前满分是60
    recordLine = sys.argv[2]
    newGroup = sys.argv[3]
    addInteresting(readFile, recordLine, newGroup)
    sys.exit()
