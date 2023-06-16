package com.example.project

import com.google.gson.Gson

data class Profile(
    var name: String,
    var alarmTime: String,
    var alarmMode: String,
    var optimalStep: String
) {
    fun toJson(): String {
        return Gson().toJson(this)
    }

    companion object {
        fun fromJson(json: String?): Profile? {
            return Gson().fromJson(json, Profile::class.java)
        }
    }
}