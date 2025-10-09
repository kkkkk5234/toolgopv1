<?php rror_reporting(0);
date_default_timezone_set("Asia/Ho_Chi_Minh");
#ini_set('display_errors', 1);
#ini_set('display_startup_errors', 1);        
#error_reporting(E_ALL);
$cookie_file = __DIR__ . '/cookie.txt';       
function input($text) {
    echo $text;
    return trim(fgets(STDIN));
}
function hienthi($fb_name, $dem, $loai, $id, $xujob, $xu){
date_default_timezone_set( 'Asia/Ho_Chi_Minh' );
        $kl = "\e[1;32m⌠\e[1;33m".$fb_name."\e[1;32m⌡\e[1;35m❯\e[1;36m❯\e[1;31m❯\033[1;34m[\033[1;33m".$dem."\033[1;34m]\033[1;91m ● \033[1;36m".date("H:i:s")."\033[1;31m ● \033[1;".rand(31,37)."m".$loai."\033[1;31m ● \033[1;37m".$id."\033[1;31m 
● \033[1;32m$xujob \033[1;31m●\033[1;32m $xu \n";
for($i = 0; $i < strlen($kl); $i++){echo $kl[$i];usleep(500);}
}
function cmt($token, $page_id, $msg) {
 $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, 'https://graph.facebook.com/'.$page_id.'/comments');
    $head[] = "Connection: keep-alive";
    $head[] = "Keep-Alive: 300";
    $head[] = "authority: m.facebook.com";
    $head[] = "ccept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7";
    $head[] = "accept-language: vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5";
    $head[] = "cache-control: max-age=0";
    $head[] = "upgrade-insecure-requests: 1";
    $head[] = "accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9";
    $head[] = "sec-fetch-site: none";
    $head[] = "sec-fetch-mode: navigate";
    $head[] = "sec-fetch-user: ?1";
    $head[] = "sec-fetch-dest: document";
    curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36');
    curl_setopt($ch, CURLOPT_ENCODING, '');
    curl_setopt($ch, CURLOPT_HTTPHEADER, $head);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
    curl_setopt($ch, CURLOPT_TIMEOUT, 60);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 60);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, TRUE);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Expect:'));
    $data = array('message' => $msg, 'access_token' => $token);
    curl_setopt($ch, CURLOPT_POST, count($data));
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    $access = curl_exec($ch);
    curl_close($ch);
    return json_decode($access);
}

function share($token,$idpost){
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, 'https://graph.facebook.com/me/feed?method=POST&link=https://www.facebook.com/'.$idpost.'&privacy={%27value%27:%20%27EVERYONE%27}&access_token='.$token);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'GET');
    curl_setopt($ch, CURLOPT_ENCODING, 'gzip, deflate');
    $headers = array();
    $headers[] = 'Authority: graph.facebook.com';
    $headers[] = 'Upgrade-Insecure-Requests: 1';
    $headers[] = 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36';
    $headers[] = 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9';
    $headers[] = 'Sec-Fetch-Site: none';
    $headers[] = 'Sec-Fetch-Mode: navigate';
    $headers[] = 'Sec-Fetch-User: ?1';
    $headers[] = 'Sec-Fetch-Dest: document';
    $headers[] = 'Accept-Language: vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5';
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

    $result = curl_exec($ch);
    if (curl_errno($ch)) {
        echo 'Error:' . curl_error($ch);
    }
    curl_close($ch);
    return $result;
}

function like_page_facebook($token, $fb_uid, $page_id) {
    $postFields = [
        'method' => 'post',
        'pretty' => 'false',
        'format' => 'json',
        'server_timestamps' => 'true',
        'locale' => 'en_US',
        'fb_api_req_friendly_name' => 'PageLike',
        'fb_api_caller_class' => 'graphservice',
        'client_doc_id' => '92246462512975232024543564417',
        'variables' => json_encode([
            "input" => [
                "source" => "page_profile",
                "client_mutation_id" => uniqid(),
                "page_id" => $page_id,
                "actor_id" => $fb_uid
            ]
        ]),
    ];

    $headers = [
        'Authorization: OAuth ' . $token,
        'User-Agent: Mozilla/5.0',
        'Content-Type: application/x-www-form-urlencoded',
    ];

    $ch = curl_init("https://graph.facebook.com/graphql");
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => http_build_query($postFields),
        CURLOPT_HTTPHEADER => $headers,
    ]);

    $response = curl_exec($ch);
    curl_close($ch);
    $res = json_decode($response, true);

    return isset($res['data']['page_like']['page']['does_viewer_like']) &&
           $res['data']['page_like']['page']['does_viewer_like'] == true;
}

function likevip($token, $page_id) {
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, 'https://graph.facebook.com/'.$page_id.'/likes');
    $head[] = "Connection: keep-alive";
    $head[] = "Keep-Alive: 300";
    $head[] = "authority: m.facebook.com";
    $head[] = "ccept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7";
    $head[] = "accept-language: vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5";
    $head[] = "cache-control: max-age=0";
    $head[] = "upgrade-insecure-requests: 1";
    $head[] = "accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9";
    $head[] = "sec-fetch-site: none";
    $head[] = "sec-fetch-mode: navigate";
    $head[] = "sec-fetch-user: ?1";
    $head[] = "sec-fetch-dest: document";
    curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36');
    curl_setopt($ch, CURLOPT_ENCODING, '');
    curl_setopt($ch, CURLOPT_HTTPHEADER, $head);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
    curl_setopt($ch, CURLOPT_TIMEOUT, 60);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 60);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, TRUE);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Expect:'));
    $data = array('access_token' => $token);
    curl_setopt($ch, CURLOPT_POST, count($data));
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    $access = curl_exec($ch);
    curl_close($ch);
    return json_decode($access);

}
function follow($token, $idpost) {
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, 'https://graph.facebook.com/' . $idpost. '/subscribers');

    $headers = [
        "Connection: keep-alive",
        "Keep-Alive: 300",
        "Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7",
        "Accept-Language: vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control: max-age=0",
        "Upgrade-Insecure-Requests: 1",
        "Accept: application/json",
        "Expect:"
    ];

    curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)');
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_TIMEOUT, 60);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 60);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);

    $postData = ['access_token' => $token];
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($postData));

    $response = curl_exec($ch);
    curl_close($ch);

    return json_decode($response, true);
}

function like($token, $page_id) {
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, 'https://graph.facebook.com/'.$page_id.'/likes');
    $head[] = "Connection: keep-alive";
    $head[] = "Keep-Alive: 300";
    $head[] = "authority: m.facebook.com";
    $head[] = "ccept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7";
    $head[] = "accept-language: vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5";
    $head[] = "cache-control: max-age=0";
    $head[] = "upgrade-insecure-requests: 1";
    $head[] = "accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9";
    $head[] = "sec-fetch-site: none";
    $head[] = "sec-fetch-mode: navigate";
    $head[] = "sec-fetch-user: ?1";
    $head[] = "sec-fetch-dest: document";
    curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36');
    curl_setopt($ch, CURLOPT_ENCODING, '');
    curl_setopt($ch, CURLOPT_HTTPHEADER, $head);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
    curl_setopt($ch, CURLOPT_TIMEOUT, 60);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 60);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, TRUE);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Expect:'));
    $data = array('access_token' => $token);
    curl_setopt($ch, CURLOPT_POST, count($data));
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    $access = curl_exec($ch);
    curl_close($ch);
    return json_decode($access);

}


function curl_post($url, $data, $headers = []) {
    global $cookie_file;
    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => is_array($data) ? http_build_query($data) : $data,
        CURLOPT_COOKIEJAR => $cookie_file,
        CURLOPT_COOKIEFILE => $cookie_file,
        CURLOPT_HTTPHEADER => $headers,
    ]);
    $res = curl_exec($ch);
    curl_close($ch);
    return $res;
}


function curl_get($url, $headers = []) {
    global $cookie_file;
    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_COOKIEJAR => $cookie_file,
        CURLOPT_COOKIEFILE => $cookie_file,
        CURLOPT_HTTPHEADER => $headers,
    ]);
    $res = curl_exec($ch);
    curl_close($ch);
    return $res;
}

function printSlow($text, $delay = 20000) {
    $chars = str_split($text);
    foreach ($chars as $char) {
        echo $char;
        usleep($delay); // micro giây (1000 = 1ms, 20000 = 20ms)
    }
    echo "\n";
}
@system('clear');
function delay ($delay){

        for($tt = $delay ;$tt>= 1;$tt--){
        echo "\r\033[1;33m   TTC_FB \033[1;31m ~>       \033[1;32m LO      \033[1;31m | $tt | "; usleep(150000);
        echo "\r\033[1;31m   TTC_FB \033[0;33m   ~>     \033[0;37m LOA     \033[0;31m | $tt | "; usleep(150000);
        echo "\r\033[1;32m   TTC_FB \033[0;33m     ~>   \033[0;37m LOAD    \033[0;31m | $tt | "; usleep(150000);
        echo "\r\033[1;34m   TTC_FB \033[0;33m       ~> \033[0;37m LOADI   \033[0;31m | $tt | "; usleep(150000);
        echo "\r\033[1;35m   TTC_FB \033[0;33m        ~>\033[0;37m LOADIN  \033[0;31m | $tt | "; usleep(150000);
        echo "\r\033[1;35m   TTC_FB \033[0;33m        ~>\033[0;37m LOADING \033[0;31m | $tt | "; usleep(150000);
        echo "\r\033[1;35m   TTC_FB \033[0;33m        ~>\033[0;37m LOADING.\033[0;31m | $tt | ";usleep(150000);}
echo "\r\e[1;95m    ⋆˚✿˖°Shop Tkhanh✿      TTC FACEBOOK               \r";
}

/////////LOGO///////////
    $xnhac = "\033[1;36m";
    $do = "\033[1;31m";
    $luc = "\033[1;32m";
    $vang = "\033[1;33m";
    $xduong = "\033[1;34m";
    $hong = "\033[1;35m";
    $trang = "\033[1;37m";
     $thanhngang = "\033[1;31m────────────────────────────────────────────────\n";
$thanh_dep = $do."[".$trang ."=.=".$do."] ".$trang."=> ";
$thanh_xau = $do."[".$trang ."VIP".$do."] ".$trang."=> ";
function logo() {
@system('clear');
    $colors = [
        "\033[1;31m", // Đỏ
        "\033[1;33m", // Vàng
        "\033[1;32m", // Xanh lá
        "\033[1;36m", // Xanh ngọc
        "\033[1;34m", // Xanh dương
        "\033[1;35m", // Tím
        "\033[1;37m"  // Trắng
    ];

    $xnhac = "\033[1;36m";
    $do = "\033[1;31m";
    $luc = "\033[1;32m";
    $vang = "\033[1;33m";
    $xduong = "\033[1;34m";
    $hong = "\033[1;35m";
    $trang = "\033[1;37m";


    $logo = [
    ];

    foreach ($logo as $i => $line) {
        echo $colors[$i % count($colors)];
        printSlow($line, 2000); // In từng dòng với hiệu ứng chậm
    }

    $thanhngang = "\033[1;31m────────────────────────────────────────────────\n";
    echo "\033[0m";
    echo "\n\033[1;33m";
    printSlow("═════════════ THÔNG TIN LIÊN HỆ ═════════════", 2000);
    echo "\033[0m";
    echo "\033[1;31m Zalo: \033[0m";  printSlow("https://zalo.me/0854533557", 2000);
    echo "\033[1;31m Tiktok:     \033[0m";  printSlow("https://www.tiktok.com/@tk_a_hplus", 2000);
    echo "\033[1;31m Facebook:  \033[0m";  printSlow("https://www.facebook.com/tkhanh223", 2000);
    echo $thanhngang;
}
logo();
// ... các đoạn trên không đổi ...

// === NHẬP TOKEN TTC ===
$ttc_token_file = __DIR__ . '/ttc_token.txt';
if (file_exists($ttc_token_file)) {
    $old = trim(file_get_contents($ttc_token_file));
    $use_old = strtolower(input("$thanh_dep Dùng lại token TTC cũ$luc y$vang /$do n$vang :$hong "));
    if ($use_old === 'y') {
        $ttc_token = $old;
    } else {
        $ttc_token = input("$thanh_dep Nhập token TTC:$vang ");
        file_put_contents($ttc_token_file, $ttc_token);
    }
} else {
    $ttc_token = input("$thanh_dep $luc Nhập token TTC:$vang ");
    file_put_contents($ttc_token_file, $ttc_token);
}
logo();///llogo
$login = curl_post('https://tuongtaccheo.com/logintoken.php', ['access_token' => $ttc_token]);
$data = json_decode($login, true);
if ($data['status'] != 'success') die("$do Login TTC thất bại\n");
echo "$hong =====$luc LOGIN TTC THÀNH CÔNG$hong =====\n";
echo"$thanh_xau$luc NAME:$vang {$data['data']['user']}\n";
echo"$thanh_xau$luc Số Dư:$vang " . number_format($data['data']['sodu'], 0, ',', '.') . " xu\n";
echo"$thanhngang";
// === NHẬP DANH SÁCH TOKEN FACEBOOK ===
$fb_token_file = __DIR__ . '/fb_tokens.txt';
$fb_tokens = [];

if (file_exists($fb_token_file)) {
    $use_old_fb = strtolower(input("$thanh_dep$vang dùng lại token fb cũ$luc y$vang /$do n$vang :$hong "));
    if ($use_old_fb === 'y') {
        $fb_tokens = array_filter(array_map('trim', file($fb_token_file)));
    }
}

if (empty($fb_tokens)) {
    echo "$thanh_dep Nhập token Facebook mỗi dòng 1 token Nhấn Enter để thoát: ";
    while (true) {
        $line = trim(fgets(STDIN));
        if ($line === '') break; // nếu dòng trống thì kết thúc
        $fb_tokens[] = $line;
    }
    file_put_contents($fb_token_file, implode("\n", $fb_tokens));
}

if (count($fb_tokens) === 0) die("$do Không có token Facebook nào\r");


$delay = (int)input("$thanh_dep$luc Nhập delay:$vang ");
$limit_per_token = (int)input("$thanh_dep Bao nhiêu nhiệm vụ thì đổi token:$hong ");
$thatbai = (int)input("$thanh_dep$luc thất bại bao nhiêu thì đổi token:$vang ");
$headers = ["User-Agent: Mozilla/5.0", "X-Requested-With: XMLHttpRequest"];
$types = ['subcheo', 'likepostvipre', 'cmtcheo', 'likepagecheo', 'likepostvipcheo'];
$type_index = 0; // Chỉ số để lật loại
$token_index = 0;
$like_count = 0;
$tt = 0;
$xu = 0;
$fail_count = 0;
$tong_xu = 0;
echo"$thanhngang";
while (true) {
    $type = $types[$type_index];
    echo "$hong $type\r";
    if (!isset($fb_tokens[$token_index])) {
        $token_index = 0;
    }
    $token = $fb_tokens[$token_index];
    $uid_json = file_get_contents("https://graph.facebook.com/me?access_token=$token");
    $uid_data = json_decode($uid_json, true);

    if (!isset($uid_data['id'])) {
        echo "$do Token không hợp lệ\r";
        $token_index++;
        continue;
    }

    $fb_token = $fb_tokens[$token_index];
    $uid_json = file_get_contents("https://graph.facebook.com/me?access_token=$fb_token");
    $uid_data = json_decode($uid_json, true);

    if (!isset($uid_data['id'])) {
        echo "Token không hợp lệ, chuyển token khác...\n";
        $token_index++;
        continue;
    }

    $fb_uid = $uid_data['id'];
    $fb_name = $uid_data['name'];
    // === ĐẶT NICK ===
$datnick = curl_post(
    'https://tuongtaccheo.com/cauhinh/datnick.php',
    "iddat%5B%5D=$fb_uid&loai=fb",
    array_merge($headers, [
        "Content-Type: application/x-www-form-urlencoded; charset=UTF-8"
    ])
);
if (strpos($datnick, '1') !== false) {
#echo"$thanhngang";
 echo "$luc ĐANG CHẠY TK:$vang $fb_name $luc ID:$vang $fb_uid $luc \r";
#echo"$thanhngang";
} else {
    echo "$do CẤU HÌNH THẤT BẠI:$vang  $datnick\r";
}

if ($type == 'likepostvipcheo') {
$getpost = curl_get("https://tuongtaccheo.com/kiemtien/likepostvipcheo/getpost.php", $headers);
$posts = json_decode($getpost, true);

// Nếu phản hồi là lỗi dạng chuỗi thông báo
if (isset($posts['error'])) {
    $countdown = isset($posts['countdown']) ? $posts['countdown'] : 10;
    echo "ĐANG LẤY NHIỆM VỤ LIKE VIP | ĐỢI $countdown giây...\r";
    sleep($countdown);
    continue;
}

if (!is_array($posts)) {

    continue;
}
            $type_index++;
            if ($type_index >= count($types)) {
            $type_index = 0;
            }
foreach ($posts as $index => $post) {
    if (!is_array($post) || !isset($post['idpost']) || !isset($post['idfb'])) {
        echo "LỖI DỮ LIỆU LIKE\r";
        print_r($post);
        continue;
    }

    $idpost = $post['idpost'];
    $page_id = $post['idfb'];


        $tt++;

        if (!likevip($token, $page_id)) {
            echo "$tt | LIKE THẤT BẠI ID: $idpost\r";
            $fail_count++;

            if ($fail_count >=$thatbai) {
                echo "LIKE THẤT BẠI $thatbai CHUYỂN TK\r";
                $token_index++;
                $like_count = 0;
                $fail_count = 0;
                break;
            }

            continue;
        }

        $fail_count = 0; // reset nếu thành công

        $nhan = curl_post("https://tuongtaccheo.com/kiemtien/likepostvipcheo/nhantien.php", "id=$idpost", array_merge($headers, ["Content-Type: application/x-www-form-urlencoded; charset=UTF-8"]));
        $json = json_decode($nhan, true);
        if (isset($json['error'])) {
        echo "LIKE THẤT BẠI BỎ QUA \r";
         break; // Thoát khỏi vòng lặp
        }
        preg_match('/\d+/', $nhan, $m);
            $xujob = $m[0];
            $xu += $xujob;
            $dem = $tt;
            $loai = "LIKE VIP";
            $id = substr($idpost, -7);
            hienthi($fb_name, $dem, $loai, $id, $xujob, $xu);

        $like_count++;
        if ($like_count >= $limit_per_token) {
            echo "ĐÃ ĐỦ $limit_per_token LIKE CHUYỂN TK\r";
            $token_index++;
            $like_count = 0;
            break;
        }
        delay ($delay);
    }

     }
elseif ($type == 'cmtcheo') {
    $getpost = curl_get("https://tuongtaccheo.com/kiemtien/cmtcheo/getpost.php", $headers);
    $posts = json_decode($getpost, true);
     if (isset($posts['error'])) {

    echo "⛔ {$posts['error']} | Đợi  giây...\r";

    continue;
}
    if (!$posts) {
        echo "Không có nhiệm vụ $type \r";
        break;
    }
            $type_index++;
            if ($type_index >= count($types)) {
            $type_index = 0;
            }
    foreach ($posts as $post) {
        $page_id = basename($post['link']);
        $idpost = $post['idpost'];
        $nd_list = json_decode($post['nd'], true);
        $msg = $nd_list[array_rand($nd_list)];

        $tt++;


        if (!cmt($token, $idpost, $msg)) {
            echo "$tt | COMMENT THẤT BẠI ID: $idpost\r";
            $fail_count++;

            if ($fail_count >=$thatbai) {
                echo "COMMENT THẤT BẠI $thatbai LẦN CHUYỂN TK\r";
                $token_index++;
                $like_count = 0;
                $fail_count = 0;
                break;
            }

            continue;
        }

        $fail_count = 0; // reset nếu thành công

        $nhan = curl_post("https://tuongtaccheo.com/kiemtien/cmtcheo/nhantien.php", "id=$idpost", array_merge($headers, ["Content-Type: application/x-www-form-urlencoded; charset=UTF-8"]));
        $json = json_decode($nhan, true);
        if (isset($json['error'])) {
        echo "COMMENT THẤT BẠI BỎ QUA \r";
              break; // Thoát khỏi vòng lặp
        }
        preg_match('/\d+/', $nhan, $m);
            $xujob = $m[0];
            $xu += $xujob;
            $dem = $tt;
            $loai = "COMMENT";
            $id = substr($idpost, -7);
            hienthi($fb_name, $dem, $loai, $id, $xujob, $xu);

        $like_count++;
        if ($like_count >= $limit_per_token) {
            echo "ĐÃ ĐỦ $limit_per_token COMMENT. CHUYỂN TK\r";
            $token_index++;
            $like_count = 0;
            break;
        }

        delay ($delay);
    }

}

elseif ($type == 'likepagecheo') {
    $getpost = curl_get("https://tuongtaccheo.com/kiemtien/likepagecheo/getpost.php", $headers);
    $posts = json_decode($getpost, true);

    if (!$posts) {
        echo "$do Không có nhiệm vụ $type chờ .\r";

        break;
    }
            $type_index++;
            if ($type_index >= count($types)) {
            $type_index = 0;
            }
    foreach ($posts as $post) {
        $page_id = basename($post['link']);
        $idpost = $post['idpost'];
        $tt++;

        if (!like_page_facebook($token, $fb_uid, $page_id)) {
            echo "$tt | LIKE PAGE THẤT BẠI ID: $idpost\r";
            $fail_count++;

            if ($fail_count >=$thatbai) {
                echo "PAGE THẤT BẠI $thatbai LẦN CHUYỂN TK\r";
                $token_index++;
                $like_count = 0;
                $fail_count = 0;
                break;
            }

            continue;
        }

        $fail_count = 0; // reset nếu thành công

        $nhan = curl_post("https://tuongtaccheo.com/kiemtien/likepagecheo/nhantien.php", "id=$idpost", array_merge($headers, ["Content-Type: application/x-www-form-urlencoded; charset=UTF-8"]));
        $json = json_decode($nhan, true);
        if (isset($json['error'])) {
        echo "FOLLOW THẤT BẠI BỎ QUA \r";
            break;
        }
        preg_match('/\d+/', $nhan, $m);
            $xujob = $m[0];
            $xu += $xujob;
            $dem = $tt;
            $loai = "PAGE";
            $id = substr($idpost, -7);
            hienthi($fb_name, $dem, $loai, $id, $xujob, $xu);

        $like_count++;
        if ($like_count >= $limit_per_token) {
            echo "ĐÃ ĐỦ $limit_per_token PAGE CHUYỂN TK\r";
            $token_index++;
            $like_count = 0;
            break;
        }

        delay ($delay);
    }

}

elseif ($type == 'likepostvipre') {
$getpost = curl_get("https://tuongtaccheo.com/kiemtien/likepostvipre/getpost.php", $headers);
$posts = json_decode($getpost, true);

// Nếu phản hồi là lỗi dạng chuỗi thông báo
if (isset($posts['error'])) {
    $countdown = isset($posts['countdown']) ? $posts['countdown'] : 10;
    echo "ĐANG LẤY NHIỆM VỤ LIKE | ĐỢI $countdown giây...\r";
    sleep($countdown);
    continue;
}

// Nếu không phải mảng danh sách nhiệm vụ
if (!is_array($posts)) {

    continue;
}
            $type_index++;
            if ($type_index >= count($types)) {
            $type_index = 0;
            }
foreach ($posts as $index => $post) {
    if (!is_array($post) || !isset($post['idpost']) || !isset($post['idfb'])) {
        echo "Lỗi dữ liệu Like không hợp le\r";
        print_r($post);
        continue;
    }

    $idpost = $post['idpost'];
    $page_id = $post['idfb'];


        $tt++;

        if (!like($token, $page_id)) {
            echo "$tt | LIKE THẤT BẠI ID: $idpost\r";
            $fail_count++;

            if ($fail_count >=$thatbai) {
                echo "LIKE THẤT BẠI $thatbai LẦN CHUYỂN TK\r";
                $token_index++;
                $like_count = 0;
                $fail_count = 0;
                break;
            }

            continue;
        }

        $fail_count = 0; // reset nếu thành công

        $nhan = curl_post("https://tuongtaccheo.com/kiemtien/likepostvipre/nhantien.php", "id=$idpost", array_merge($headers, ["Content-Type: application/x-www-form-urlencoded; charset=UTF-8"]));
        $json = json_decode($nhan, true);
        if (isset($json['error'])) {
        echo "LIKE THẤT BẠI BỎ QUA \r";
              break; // Thoát khỏi vòng lặp
        }
        preg_match('/\d+/', $nhan, $m);
            $xujob = $m[0];
            $xu += $xujob;
            $dem = $tt;
            $loai = "LIKE";
            $id = substr($idpost, -7);
            hienthi($fb_name, $dem, $loai, $id, $xujob, $xu);
        $like_count++;
        if ($like_count >= $limit_per_token) {
            echo "ĐÃ ĐỦ $limit_per_token LIKE CHUYỂN TK\r";
            $token_index++;
            $like_count = 0;
            break;
        }

        delay ($delay);
    }

}

elseif ($type == 'subcheo') {
    $getpost = curl_get("https://tuongtaccheo.com/kiemtien/subcheo/getpost.php", $headers);
    $posts = json_decode($getpost, true);

    if (!$posts) {
        echo "Không có nhiệm vụ $type .\r";
        break;
    }
            $type_index++;
            if ($type_index >= count($types)) {
            $type_index = 0;
            }
    foreach ($posts as $post) {
        $page_id = basename($post['link']);
        $idpost = $post['idpost'];
        $tt++;

        if (!follow($token, $idpost)) {
            echo "$tt | FOLLOW THẤT BẠI ID: $idpost\r";
            $fail_count++;

            if ($fail_count >= $thatbai) {
                echo "FOLLOW THẤT BẠI $thatbai LẦN CHUYỂN TK\r";
                $token_index++;
                $like_count = 0;
                $fail_count = 0;
                break;
            }

            continue;
        }

        $fail_count = 0; // reset nếu thành công
        $nhan = curl_post("https://tuongtaccheo.com/kiemtien/subcheo/nhantien.php", "id=$idpost", array_merge($headers, ["Content-Type: application/x-www-form-urlencoded; charset=UTF-8"]));
        $json = json_decode($nhan, true);
        if (isset($json['error'])) {
        echo "FOLLOW THẤT BẠI BỎ QUA \r";
                break; // Thoát khỏi vòng lặp
        }
        preg_match('/\d+/', $nhan, $m);
            $xujob = $m[0];
            $xu += $xujob;
            $dem = $tt;
            $loai = "FOLLOW";
            $id = substr($idpost, -7);
            hienthi($fb_name, $dem, $loai, $id, $xujob, $xu);
        $like_count++;
        if ($like_count >= $limit_per_token) {
            echo "ĐÃ ĐỦ $limit_per_token FOLLOW CHUYỂN TÀI KHOẢN\r";
            $token_index++;
            $like_count = 0;
            break;
        }

        delay ($delay);
    }

}

}  
