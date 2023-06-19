package com.example.project

// 기능 : fragment 간에 firstLaunch의 인자를 공유해서 사용하기 위해 사용
object SharedData {
    var firstLaunch: FirstLaunch = FirstLaunch()
}