package com.example.project

import com.google.gson.Gson
// 기능 : Profile 데이터 클래스를 정의하고 JSON의 직렬화 및 역직렬화를 수행
data class Profile(
    var name: String,
    var alarmTime: String,
    var alarmMode: String,
    var optimalStep: String
) {
    // 기능 : Profile 객체를 JSON 문자열로 직렬화
    fun toJson(): String {
        return Gson().toJson(this)
    }
    // 클래스의 인스턴스 생성 없이 직접 접근 가능
    companion object {
        fun fromJson(json: String?): Profile? {
            return Gson().fromJson(json, Profile::class.java)
        }
    }
}