package com.example.project.ui.addprofile

import android.content.Context
import android.content.SharedPreferences
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.EditText
import android.widget.Switch
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import com.example.project.R
import com.example.project.Profile
import com.example.project.ui.profilelist.ProfileListFragment


class AddProfileFragment : Fragment() {

    private var selectedAlarmMode: String? = null
    private var isAlarmOn: Boolean = false

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val view = inflater.inflate(R.layout.fragment_addprofile, container, false)

        val profileNameEditText = view.findViewById<EditText>(R.id.profileNameEditText)
        val profileAlarmTimeEditText = view.findViewById<EditText>(R.id.addProfileAlarmTimeEditText)

        val alarmSwitch = view.findViewById<Switch>(R.id.addAlarmSwitch)
        val alarmSoundmodeButton = view.findViewById<Button>(R.id.addAlarmSoundmodeButton)
        val alarmVibemodeButton = view.findViewById<Button>(R.id.addAlarmVibemodeButton)
        val alarmSoundvibemodeButton = view.findViewById<Button>(R.id.addAlarmSoundvibemodeButton)

        alarmSwitch.isChecked = false
        alarmSoundmodeButton.isEnabled = false
        alarmVibemodeButton.isEnabled = false
        alarmSoundvibemodeButton.isEnabled = false
        profileAlarmTimeEditText.isEnabled = false

        alarmSoundmodeButton.setOnClickListener { selectAlarmMode("소리") }
        alarmVibemodeButton.setOnClickListener { selectAlarmMode("진동") }
        alarmSoundvibemodeButton.setOnClickListener { selectAlarmMode("소리 / 진동") }

        val addProfileButton = view.findViewById<Button>(R.id.addProfileButton)

        alarmSwitch.setOnCheckedChangeListener { _, isChecked ->
            isAlarmOn = isChecked
            if (isChecked) {
                alarmSoundmodeButton.isEnabled = true
                alarmVibemodeButton.isEnabled = true
                alarmSoundvibemodeButton.isEnabled = true
                profileAlarmTimeEditText.isEnabled = true
                Toast.makeText(requireContext(), "알람 ON : 알람 세부사항을 설정해주세요", Toast.LENGTH_SHORT).show()
            } else {
                alarmSoundmodeButton.isEnabled = false
                alarmVibemodeButton.isEnabled = false
                alarmSoundvibemodeButton.isEnabled = false
                profileAlarmTimeEditText.isEnabled = false
                Toast.makeText(requireContext(), "알람 OFF", Toast.LENGTH_SHORT).show()
            }
        }

        addProfileButton.setOnClickListener {
            val name = profileNameEditText.text.toString()
            if (name.isBlank()) {
                Toast.makeText(requireContext(), "이름을 입력해주세요.", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }
            val alarmTime = if (profileAlarmTimeEditText.text.toString().isNotBlank()) {
                profileAlarmTimeEditText.text.toString()
            } else {
                "미설정"
            }
            val alarmMode = selectedAlarmMode ?: "미설정"
            val optimalStep = "미설정"
            val profile = Profile(name, alarmTime, alarmMode, optimalStep)
            addProfile(requireContext(), profile)
            Toast.makeText(requireContext(), "프로필이 추가되었습니다.", Toast.LENGTH_SHORT).show()

            val sharedPreferences = requireContext().getSharedPreferences(PROFILE_PREFS_KEY, Context.MODE_PRIVATE)
            with(sharedPreferences.edit()) {
                putString("selected_profile", profile.name)
                commit()
            }

            val profileJson = profile.toJson()
            findNavController().navigate(R.id.action_addProfileFragment_to_profileListFragement)

        }

        return view
    }

    private fun selectAlarmMode(alarmMode: String) {
        selectedAlarmMode = alarmMode
        Toast.makeText(requireContext(), "선택된 알람 모드: $alarmMode", Toast.LENGTH_SHORT).show()
    }

    companion object {
        const val PROFILE_PREFS_KEY = "profile_prefs_key"

        fun addProfile(context: Context, profile: Profile) {
            val sharedPreferences = context.getSharedPreferences(PROFILE_PREFS_KEY, Context.MODE_PRIVATE)
            with(sharedPreferences.edit()) {
                putString(profile.name, profile.toJson())
                commit()
            }
        }
    }
}