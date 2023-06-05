package com.example.project.ui.heightcontrolloer

import android.content.Context
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import com.example.project.Profile
import com.example.project.databinding.FragmentHeightcontrollerBinding
import androidx.lifecycle.ViewModelProvider
import com.example.project.PacketViewModel

class HeightControllerFragment : Fragment() {

    private lateinit var packetViewModel: PacketViewModel

    private var _binding: FragmentHeightcontrollerBinding? = null
    private val binding get() = _binding!!

    private var currentStep = 0

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentHeightcontrollerBinding.inflate(inflater, container, false)

        packetViewModel = ViewModelProvider(requireActivity()).get(PacketViewModel::class.java)

        binding.stepInputButton.setOnClickListener {
            val inputText = binding.stepEdittext.text.toString()
            if (inputText.isNotEmpty()) {
                currentStep = inputText.toInt()
                updateNowStepText()
                binding.stepEdittext.text = null
                packetViewModel.updateParameter0(currentStep.toString())
                packetViewModel.logPacketData()
            }
        }

        binding.stepUpButton.setOnClickListener {
            currentStep++
            updateNowStepText()
            packetViewModel.updateParameter0(currentStep.toString())
            packetViewModel.logPacketData()
        }

        binding.stepDownButton.setOnClickListener {
            currentStep--
            updateNowStepText()
            packetViewModel.updateParameter0(currentStep.toString())
            packetViewModel.logPacketData()
        }

        binding.saveButton.setOnClickListener {
            val selectedProfileName = packetViewModel.getSelectedProfileName(requireContext())
            if (selectedProfileName != null) {
                val profileJson = packetViewModel.getProfileJson(requireContext(), selectedProfileName)
                if (profileJson != null) {
                    var profile = Profile.fromJson(profileJson)
                    profile?.let {
                        it.optimalStep = currentStep.toString()
                        packetViewModel.saveProfile(requireContext(), it)
                        Toast.makeText(requireContext(), "현재 단계가 저장되었습니다.", Toast.LENGTH_SHORT)
                            .show()
                    }
                }
            }
        }

        if (savedInstanceState != null) {
            currentStep = savedInstanceState.getInt("currentStep", 0)
            updateNowStepText()
        }

        return binding.root
    }

    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        outState.putInt("currentStep", currentStep)
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }

    private fun updateNowStepText() {
        binding.nowStep.text = currentStep.toString()
    }

    companion object {
        private const val PROFILE_PREFS_KEY = "profile_prefs_key"

        fun saveProfile(context: Context, profile: Profile) {
            val sharedPreferences = context.getSharedPreferences(PROFILE_PREFS_KEY, Context.MODE_PRIVATE)
            sharedPreferences.edit().apply {
                putString(profile.name, profile.toJson())
                commit()
            }
        }
    }
}