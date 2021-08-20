import math

def standardizeTeamName(str, withError):
    if (str == "San JosÃ© State"):
        return ("San Jose St.")
    if (len(str.split("San Jos")) > 1):
        return ("San Jose St.")
    name = str.lower()
    if (name == "air force" or name == "a. force" or name == "afa" or name == "af"):
        return ("Air Force")
    elif (name == "akron"):
        return ("Akron")
    elif (name == "alabama" or name == "ala."):
        return ("Alabama")
    elif (name == "appalachian state" or name == "app. st." or name == "appalachian st." or name == "appalach. st" or name == "app. st" or name == "appalachian st" or name == "app st." or name == "app"):
        return ("App St.")
    elif (name == "arizona"):
        return ("Arizona")
    elif (name == "arizona state" or name == "arizona st." or name == "arizona st" or name == "ariz. st." or name == "ariz. st" or name == "ariz.st." or name == "arizon st." or name == "az. st."):
        return ("Arizona St.")
    elif (name == "arkansas" or name == "ark."):
        return ("Arkansas")
    elif (name == "arkansas state" or name == "arkansas st." or name == "ark. st." or name == "arkansas st" or name == "ark. st" or name == "ark st."):
        return ("Arkansas St.")
    elif (name == "army west point" or name == "army"):
        return ("Army")
    elif (name == "auburn"):
        return ("Auburn")
    elif (name == "ball state" or name == "ball st." or name == "ball st"):
        return ("Ball St.")
    elif (name == "baylor"):
        return ("Baylor")
    elif (name == "boise state" or name == "boise st." or name == "boise st"):
        return ("Boise St.")
    elif (name == "boston college" or name == "boston col." or name == "bost. col." or name == "boston coll." or name == "bost col" or name == "bost col." or name == "boston col" or name == "bost. coll." or name == "bos. col." or name == "bost. college" or name == "boston coll" or name == "bost coll." or name == "bcu"):
        return ("Boston College")
    elif (name == "bowling green" or name == "b. green" or name == "bowling grn" or name == "bowl. green" or name == "bowling gr." or name == "bowl. gr." or name == "bowl.green" or name == "bowl.grn." or name == "bowl. grn" or name == "bowl. grn." or "bowl" in name or name == "bgsu"):
        return ("Bowling Green")
    elif (name == "buffalo"):
        return ("Buffalo")
    elif (name == "byu"):
        return ("BYU")
    elif (name == "california" or name == "califrnia" or name == "cal" or name == "cal."):
        return ("Cal")
    elif (name == "central michigan" or name == "c. michigan" or name == "c. mich." or name == "c. mich" or name == "c. mich" or name == "centrl michigan" or name == "central mich" or name == "cmu"):
        return ("Central Michigan")
    elif (name == "charlotte"):
        return ("Charlotte")
    elif (name == "cincinnati" or name == "cincy" or name == "cinn."):
        return ("Cincinnati")
    elif (name == "clemson" or name == "clem." or name == "clem"):
        return ("Clemson")
    elif (name == "coastal carolina" or name == "coastal car." or name == "coast. car" or name == "coast. car." or name == "coast car" or name == "coas. car" or name == "coastl carolina"):
        return ("Coastal Carolina")
    elif (name == "colorado" or name == "colo." or name == "col."):
        return ("Colorado")
    elif (name == "colorado state" or name == "colorado st." or name == "colo. st." or name == "colorado st" or name == "colo. st" or name == "col. st." or name == "col st."):
        return ("Colorado St.")
    elif (name == "connecticut" or name == "conn." or name == "conn" or name == "uconn" or name == "uconn."):
        return ("UConn")
    elif (name == "duke"):
        return ("Duke")
    elif (name == "east carolina" or name == "e. carolina" or name == "e. carol." or name == "ecu" or name == "e. car." or name == "east car." or name == "e. car" or name == "eastrn carolina" or name == "eastcrlina"):
        return ("ECU")
    elif (name == "eastern michigan" or name == "e. michigan" or name == "e. mich." or name == "e. mich" or name == "eastrn michigan" or name == "east mich"):
        return ("Eastern Michigan")
    elif (name == "florida"):
        return ("Florida")
    elif (name == "florida atlantic" or name == "florida atl." or name == "fla. atl." or name == "fla. atlantic" or name == "fla atlantic" or name == "fau"):
        return ("FAU")
    elif (name == "florida international" or name == "florida int." or name == "fla. int." or name == "fiu" or name == "fla. intl." or name == "florida intl." or name == "fla.-int'l" or name == "fiu" or name == "florida int'l" or name == "florida intl"):
        return ("FIU")
    elif (name == "florida state" or name == "florida st." or name == "florida st" or name == "fla. st" or name == "fla. st." or name == "fla .st." or name == "fla st."):
        return ("Florida St.")
    elif (name == "fresno state" or name == "fresno st." or name == "fresno st" or name == "fres. st."):
        return ("Fresno St.")
    elif (name == "georgia"):
        return ("Georgia")
    elif (name == "georgia southern" or name == "georgia so." or name == "ga. so." or name == "ga. southern" or name == "ga southern" or name == "ga. south."):
        return ("Georgia Southern")
    elif (name == "georgia state" or name == "georgia st." or name == "ga st." or name == "georgia st" or name == "ga st" or name == "ga. st."):
        return ("Georgia St.")
    elif (name == "georgia tech" or name == "ga. tech" or name == "ga tech" or name == "geogia tech"):
        return ("Georgia Tech")
    elif (name == "hawaii" or name == "hawai'i"):
        return ("Hawaii")
    elif (name == "houston" or name == "houst" or name == "hou"):
        return ("Houston")
    elif (name == "idaho"):
        return ("Idaho")
    elif (name == "illinois" or name == "lllinois"):
        return ("Illinois")
    elif (name == "indiana" or name == "ind"):
        return ("Indiana")
    elif (name == "iowa"):
        return ("Iowa")
    elif (name == "iowa state" or name == "iowa st." or name == "iowa st"):
        return ("Iowa St.")
    elif (name == "kansas"):
        return ("Kansas")
    elif (name == "kansas state" or name == "kansas st." or name == "kan st." or name == "kan. st." or name == "kansas st" or name == "kan st" or name == "kan. st" or name == "kansasst"):
        return ("Kansas St.")
    elif (name == "kent state" or name == "kent st." or name == "kent st"):
        return ("Kent St.")
    elif (name == "kentucky" or name == "kent'ky" or name == "kent" or name == "uk"):
        return ("Kentucky")
    elif (name == "liberty"):
        return ("Liberty")
    elif (name == "louisiana lafayette" or name == "louisiana" or name == "la.-laf" or name == "la.-laff" or name == "la.-lafayette" or name == "la.-laf." or name == "la.-laff" or name == "la.-laff." or name == "lafayette" or name == "la.-lafay." or name == "la. laf." or name == "louisiana-lafayette" or name == "la.-lafayete" or name == "la lafayette" or name == "la.-lafay" or "lafay" in name):
        return ("LA Lafayette")
    elif (name == "louisiana monroe" or name == "la.-mon" or name == "la-mnroe" or name == "la.-monroe" or name == "la.-mon." or name == "la-monroe" or name == "la. monroe" or name == "la. mon." or name == "louisiana-monroe" or name == "la monroe" or name == "ul monroe" or name == "ulm"):
        return ("LA Monroe")
    elif (name == "louisiana tech" or name == "la tech" or name == "la. tech" or name == "la .tech" or name == "latech" or name == "latech"):
        return ("LA Tech")
    elif (name == "louisville" or name == "l'ville" or name == "lv"):
        return ("Louisville")
    elif (name == "lsu"):
        return ("LSU")
    elif (name == "marshall" or name == "marsh."):
        return ("Marshall")
    elif (name == "maryland" or name == "mary."):
        return ("Maryland")
    elif (name == "massachusetts" or name == "mass." or name == "mass" or name == "umass"):
        return ("UMass")
    elif (name == "memphis" or name == "mem "):
        return ("Memphis")
    elif (name == "miami-florida" or name == "miami-fla." or name == "miami-fla" or name == "miami" or name == "miami-fl" or name == "miami fl" or name == "mia.-fla." or name == "mia-fla" or ("mia" in name and "fla" in name) or name == "miami florida"):
        return ("Miami-FL")
    elif (name == "miami-ohio" or name == "miami-o." or name == "miami (oh)" or "-oh" in name or name == "miami oh" or name == "miami ohio"):
        return ("Miami-Ohio")
    elif (name == "michigan" or name == "mich."):
        return ("Michigan")
    elif (name == "michigan state" or name == "michigan st." or name == "mich. st." or name == "mich st." or name == "mich.st." or name == "mich. st" or name == "michigan st" or name == "mich st" or name == "mich.st"):
        return ("Michigan St.")
    elif (name == "middle tennessee" or name == "mtsu" or name == "m. tenn. st." or name == "m. tenn. st" or name == "middle tennessee state" or name == "m.tenn st." or name == "m.tenn. st." or name == "mid. tenn. st." or name == "mid.tenn. st." or name == "mid tenn. st." or name == "m. tn. st." or name == "md. tenn. st." or "m.tenn" in name or name == "m tenn. st." or name == "middle tenn"):
        return ("MTSU")
    elif (name == "minnesota" or name == "minn." or name == "minn"):
        return ("Minnesota")
    elif (name == "mississippi" or name == "miss." or name == "ole miss" or name == "ole miss." or name == "miss"):
        return ("Ole Miss")
    elif (name == "mississippi state" or name == "mississippi st." or name == "miss. st." or name == "mississippi st" or name == "miss. st" or name == "miss state" or name == "miss st" or name == "miss. state" or name == "miss st." or name == "miss.st."):
        return ("Mississippi St.")
    elif (name == "missouri" or name == "missourii" or name == "misso"):
        return ("Missouri")
    elif (name == "navy"):
        return ("Navy")
    elif (name == "nebraska" or name == "nebr."):
        return ("Nebraska")
    elif (name == "nevada"):
        return ("Nevada")
    elif (name == "new mexico" or name == "n. mexico" or name == "n. mex." or name == "new mex." or name == "nmex"):
        return ("New Mexico")
    elif (name == "new mexico state" or name == "n. mexico st." or name == "n. mex. st." or name == "n. mexico st" or name == "n. mex. st" or name == "n. mex st" or name == "new mexico st." or name == "new mexico st" or name == "new mex. st." or name == "n. mex st."):
        return ("New Mexico St.")
    elif (name == "north carolina" or name == "n. carolina" or name == "n. carol." or name == "n. car." or name == "no. carolina"):
        return ("North Carolina")
    elif (name == "north carolina state" or name == "n. carolina st." or name == "n. car. st." or name == "north carolina st." or name == "n. carolina st" or name == "n. car. st" or name == "north carolina st" or name == "n. carolina st.." or name == "nc state" or name == "nc st." or name == "n. c. st." or name == "n. car.st." or name == "north car. st." or name == "n.c. st."):
        return ("NC St.")
    elif (name == "north texas" or name == "n. texas" or name == "no. texas" or name == "no.texas"):
        return ("North Texas")
    elif (name == "northern illinois" or name == "n. illinois" or name == "uni" or name == "northern  illinois" or name == "no. illinois" or name == "n. ill." or name == "no. ill." or name == "n. ill" or name == "northn illinois" or name == "northernil"):
        return ("Northern Illinois")
    elif (name == "northwestern" or name == "n'western" or name == "n'westrn" or name == "no'western" or name == "n’western" or name == "n’westrn" or name == "no’western" or name == "n'wstrn" or name == "n'w'stern" or name == "n'wstern" or name == "nw" or name == "n'w"):
        return ("Northwestern")
    elif (name == "notre dame" or name == "n. dame"):
        return ("Notre Dame")
    elif (name == "ohio university" or name == "ohio" or name == "ohio u." or name == "ohio u"):
        return ("Ohio")
    elif (name == "ohio state" or name == "ohio st." or name == "ohio st" or name == "ohiost"):
        return ("Ohio St.")
    elif (name == "oklahoma" or name == "okla."):
        return ("Oklahoma")
    elif (name == "oklahoma state" or name == "oklahoma st." or name == "okla. st." or name == "okla. st" or name == "oklahoma st" or name == "okla st" or name == "oklahoma  st." or name == "okl. st." or name == "okla st."):
        return ("Oklahoma St.")
    elif (name == "old dominion" or name == "odu" or name == "old dom." or name == "old dom" or name == "olddominion"):
        return ("Old Dominion")
    elif (name == "oregon" or name == "oregn"):
        return ("Oregon")
    elif (name == "oregon state" or name == "oregon st." or name == "ore st" or name == "oregon st" or name == "ore. st" or name == "ore. st." or name == "ore st." or name == "oreg st."):
        return ("Oregon St.")
    elif (name == "penn state" or name == "penn st." or name == "penn st"):
        return ("Penn St.")
    elif (name == "pittsburgh" or name == "pitt" or name == "pitt."):
        return ("Pitt")
    elif (name == "purdue"):
        return ("Purdue")
    elif (name == "rice"):
        return ("Rice")
    elif (name == "rutgers"):
        return ("Rutgers")
    elif (name == "san diego state" or name == "san diego st." or name == "s. diego st." or name == "san diego st" or name == "s. diego st" or name == "s diego st" or name == "s.diego st." or name == "s.d. st." or name == "sdsu" or name == "s diego st" or name == "s diego st."):
        return ("San Diego St.")
    elif (name == "san jose state" or name == "san jose st." or name == "s. jose st." or name == "san jose st" or name == "s. jose st" or name == "s jose st" or name == "s.j. st." or name == "san josé state" or name == "s.jose st." or name == "san josac state" or name == "sjsu" or name == "s jose st."):
        return ("San Jose St.")
    elif (name == "smu"):
        return ("SMU")
    elif (name == "south alabama" or name == "s. alabama"):
        return ("South Alabama")
    elif (name == "south carolina" or name == "s. carolina" or name == "so. carolina" or name == "so carolina" or name == "s. carol." or name == "s. car." or name == "so. car." or name == "s carolina" or name == "s. car"):
        return ("South Carolina")
    elif (name == "south florida" or name == "usf" or name == "s. florida" or name == "so florida" or name == "so. florida" or name == "s. fla." or name == "s florida"):
        return ("USF")
    elif (name == "southern california" or name == "usc" or name == "s. california" or name == "s. calif." or name == "s.california" or name == "so. california" or name == "so. cal" or name == "so. calif." or name == "southern cal" or name == "s. cal." or name == "s. cal" or name == "so cal" or name == "so. cal."):
        return ("USC")
    elif (name == "southern miss" or name == "s. miss" or name == "so. miss." or name == "s. mississippi" or name == "so. miss" or name == "s. miss." or name == "southern mississippi" or name == "s mississippi" or name == "usm"):
        return ("Southern Miss")
    elif (name == "stanford" or name == "stan."):
        return ("Stanford")
    elif (name == "syracuse" or name == "syr."):
        return ("Syracuse")
    elif (name == "tcu"):
        return ("TCU")
    elif (name == "temple"):
        return ("Temple")
    elif (name == "tennessee" or name == "tenn." or name == "tennesse" or name == "tenn"):
        return ("Tennessee")
    elif (name == "texas"):
        return ("Texas")
    elif (name == "texas a&m" or name == "tex. a&m" or name == "texas am"):
        return ("Texas A&M")
    elif (name == "texas state" or name == "texas st." or name == "texas st" or name == "txst"):
        return ("Texas St.")
    elif (name == "texas tech" or name == "tx. tech" or name == "tex. tech" or name == "tex.tech" or ("tex" in name and "tech" in name)):
        return ("Texas Tech")
    elif (name == "toledo"):
        return ("Toledo")
    elif (name == "troy" or name == "troy st." or name == "troy state"):
        return ("Troy")
    elif (name == "tulane"):
        return ("Tulane")
    elif (name == "tulsa"):
        return ("Tulsa")
    elif (name == "uab"):
        return ("UAB")
    elif (name == "ucf" or name == "central florida" or name == "c. florida" or name == "central fla." or name == "c. fla." or name == "cent. fla."):
        return ("UCF")
    elif (name == "ucla"):
        return ("UCLA")
    elif (name == "unlv"):
        return ("UNLV")
    elif (name == "utah"):
        return ("Utah")
    elif (name == "utah state" or name == "utah st." or name == "utah st"):
        return ("Utah St.")
    elif (name == "utep" or name == "texas-el paso" or name == "tx.-el paso"):
        return ("UTEP")
    elif (name == "utsa" or name == "ut san antonio" or name == "texassan"):
        return ("UTSA")
    elif (name == "vanderbilt" or name == "vandy"):
        return ("Vanderbilt")
    elif (name == "virginia"):
        return ("Virginia")
    elif (name == "virginia tech" or name == "va. tech" or name == "virg. tech" or name == "va.tech"):
        return ("Virginia Tech")
    elif (name == "wake forest" or name == "w. forest" or name == "w. for." or name == "wake for." or name == "wake f." or "wake" in name or name == "wfrst"):
        return ("Wake Forest")
    elif (name == "washington" or name == "wash." or name == "wash"):
        return ("Washington")
    elif (name == "washington state" or name == "washington st." or name == "wash. st." or name == "wash. st" or name == "washington st" or name == "wash. state" or name == "wash st." or name == "wash.st."):
        return ("Washington St.")
    elif (name == "west virginia" or name == "w. virginia" or name == "w. va." or name == "west va." or name == "w. virg."):
        return ("West Virginia")
    elif (name == "western kentucky" or name == "wku" or name == "w. ky." or name == "w. kentucky" or name == "western ky" or name == "w. kent'ky" or name == "w. ky" or name == "w. kent'cky" or name == "w. kent." or name == "westrn kentucky"):
        return ("WKU")
    elif (name == "western michigan" or name == "w. michigan" or name == "w. mich." or name == "w. mich" or name == "westrn michigan" or name == "wmu"):
        return ("Western Michigan")
    elif (name == "wisconsin" or name == "wisc." or name == "wisc"):
        return ("Wisconsin")
    elif (name == "wyoming" or name == "wyo." or name == "wyo" or name == "wym." or name == "wyom"):
        return ("Wyoming")
    else:
        if (withError):
            return ("Error: " + str.title())
        return (str.title())

#for spreads
def getBin(a, W12 = False, W1 = False, W234 = False):
    b = abs(float(a))
    if (W12):
        if (b <= 2.5):
            return 0
        elif (b <= 3.5):
            return 3
        elif (b <= 5):
            return 4
        elif (b <= 6.5):
            return 6
        elif (b <= 7.5):
            return 7
        elif (b <= 9.5):
            return 8
        elif (b <= 12.5):
            return 10
        elif (b <= 14):
            return 13
        elif (b <= 16.5):
            return 14.5
        elif (b <= 18.5):
            return 17
        elif (b <= 21):
            return 19
        elif (b <= 24):
            return 21.5
        elif (b <= 28):
            return 24.5
        else:
            return -1
    elif (W1):
        if (b <= 2.5):
            return 0
        elif (b <= 3.5):
            return 3
        elif (b <= 6.5):
            return 4
        elif (b <= 9.5):
            return 7
        elif (b <= 12.5):
            return 10
        elif (b <= 16.5):
            return 13
        elif (b <= 18.5):
            return 17
        elif (b <= 21):
            return 19
        elif (b <= 24):
            return 21.5
        elif (b <= 28):
            return 24.5
        else:
            return -1
    elif (W234):
        if (b <= 2):
            return 0
        elif (b <= 7.5):
            return math.trunc(b)
        elif (b <= 9.5):
            return 8
        elif (b <= 12.5):
            return 10
        elif (b <= 14):
            return 13
        elif (b <= 16.5):
            return 14.5
        elif (b <= 18.5):
            return 17
        elif (b <= 21):
            return 19
        elif (b <= 24):
            return 21.5
        elif (b <= 28):
            return 24.5
        else:
            return -1
    else:
        if (b <= 18):
            return b
        elif (b <= 19):
            return 18.5
        elif (b <= 20):
            return 19.5
        elif (b <= 21.5):
            return b
        elif (b <= 22.5):
            return 22
        elif (b <= 28.5):
            return math.trunc(b)
        else:
            return -1

def getTotalBin(a):
    b = abs(float(a))
    if (b >= 78 and b <= 80.5):
        return 78
    elif (b >= 37 and b <= 38.5):
        return 37
    elif (b < 37 or b > 80.5):
        return -1
    elif (b >= 44 and b <= 66.5):
        return b
    else:
        return math.trunc(b)
