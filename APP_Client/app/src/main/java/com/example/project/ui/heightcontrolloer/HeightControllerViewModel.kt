package com.example.project.ui.heightcontrolloer

import android.content.SharedPreferences
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.example.project.Profile

class HeightControllerViewModel(private val sharedPreferences: SharedPreferences) : ViewModel() {

    private val _currentStep = MutableLiveData<Int>()
    val currentStep: MutableLiveData<Int>
        get() = _currentStep

    init {
        // 초기값 설정
        _currentStep.value = 0
    }

    fun setCurrentStep(step: Int) {
        _currentStep.value = step
    }

    fun incrementStep() {
        val step = _currentStep.value ?: 0
        _currentStep.value = step + 1
    }

    fun decrementStep() {
        val step = _currentStep.value ?: 0
        _currentStep.value = step - 1
    }

    fun getSelectedProfileName(): String? {
        return sharedPreferences.getString("selected_profile", null)
    }

    fun getProfileJson(profileName: String): String? {
        return sharedPreferences.getString(profileName, null)
    }

    fun getCurrentStep(): Int {
        return currentStep.value ?: 0
    }

    fun saveProfile(profile: Profile) {
        with(sharedPreferences.edit()) {
            putString(profile.name, profile.toJson())
            commit()
        }
    }
}