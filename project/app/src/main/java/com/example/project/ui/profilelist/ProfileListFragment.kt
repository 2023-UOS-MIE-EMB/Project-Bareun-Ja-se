package com.example.project.ui.profilelist

import NetworkManager
import android.content.Context
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import androidx.navigation.fragment.findNavController
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.project.PacketViewModel
import com.example.project.Profile
import com.example.project.R
import com.example.project.ui.addprofile.AddProfileFragment.Companion.PROFILE_PREFS_KEY

class ProfileListFragment : Fragment() {

    private lateinit var profileRecyclerView: RecyclerView
    private lateinit var profileAdapter: ProfileAdapter
    private var profileList: List<Profile> = emptyList()
    private val networkManager = NetworkManager()

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        val view = inflater.inflate(R.layout.fragment_profilelist, container, false)
        profileRecyclerView = view.findViewById(R.id.profileRecyclerView)
        return view
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        profileAdapter = ProfileAdapter()
        profileRecyclerView.apply {
            layoutManager = LinearLayoutManager(requireContext())
            adapter = profileAdapter
        }
        updateProfileList()
    }

    private fun updateProfileList() {
        profileList = getProfileList(requireContext())
        profileAdapter.submitList(profileList)
    }

    // 프로필 목록 가져오는 함수
    private fun getProfileList(context: Context): List<Profile> {
        // SharedPreferences 객체 생성
        val sharedPreferences = context.getSharedPreferences(PROFILE_PREFS_KEY, Context.MODE_PRIVATE)
        // SharedPreferences에서 저장된 프로필 정보 목록 가져오기
        val profileMap = sharedPreferences.all
        // 프로필 정보 목록을 Profile 객체 목록으로 변환
        return profileMap.filterKeys { it != "selected_profile" }
            .flatMap { Profile.fromJson(it.value.toString())?.let { listOf(it) } ?: emptyList() }
    }

    // 선택한 프로필 저장하는 함수
    fun saveSelectedProfile(context: Context, profile: Profile) {
        // SharedPreferences 객체 생성
        val sharedPreferences = context.getSharedPreferences(PROFILE_PREFS_KEY, Context.MODE_PRIVATE)
        // SharedPreferences에 선택된 프로필 정보 저장
        with(sharedPreferences.edit()) {
            putString("selected_profile", profile.name)
            commit()
        }
    }

    // 프로필 삭제 함수
    private fun deleteProfile(context: Context, name: String) {
        // SharedPreferences 객체 생성
        val sharedPreferences =
            context.getSharedPreferences(PROFILE_PREFS_KEY, Context.MODE_PRIVATE)
        // SharedPreferences에서 해당 이름의 프로필 정보 삭제
        with(sharedPreferences.edit()) {
            remove(name)
            commit()
        }
    }

    inner class ProfileAdapter : RecyclerView.Adapter<ProfileAdapter.ProfileViewHolder>() {
        private var profileList: List<Profile> = emptyList()

        override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ProfileViewHolder {
            val view =
                LayoutInflater.from(parent.context).inflate(R.layout.item_profile, parent, false)
            return ProfileViewHolder(view)
        }

        override fun onBindViewHolder(holder: ProfileViewHolder, position: Int) {
            val profile = profileList[position]
            holder.bind(profile)
        }

        override fun getItemCount(): Int = profileList.size

        fun submitList(newProfileList: List<Profile>) {
            profileList = newProfileList
            notifyDataSetChanged()
        }

        inner class ProfileViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
            private val profileNameTextView: TextView = itemView.findViewById(R.id.profileName)
            private val selectButton: Button = itemView.findViewById(R.id.selectProfileButton)
            private val deleteButton: Button = itemView.findViewById(R.id.deleteProfileButton)

            fun bind(profile: Profile) {
                profileNameTextView.text = profile.name

                selectButton.setOnClickListener {
                    val context = itemView.context
                    saveSelectedProfile(context, profile)

                    Toast.makeText(context, "${profile.name} 프로필이 선택되었습니다.", Toast.LENGTH_SHORT)
                        .show()

                    val packetViewModel = ViewModelProvider(requireActivity()).get(PacketViewModel::class.java)
                    if (profile.alarmTime == "미설정") {
                        packetViewModel.updateParameter3("0")
                    }else {
                        packetViewModel.updateParameter3(profile.alarmTime)
                    }

                    if (profile.alarmMode == "진동") {
                        packetViewModel.updateParameter4("1")
                    } else if (profile.alarmMode == "소리") {
                        packetViewModel.updateParameter4("2")
                    } else if (profile.alarmMode == "미설정") {
                        packetViewModel.updateParameter4("0")
                    }
                    var resultPacket: Pair<Boolean, ByteArray> = packetViewModel.makePacketToSend()
                    val isSuccess: Boolean = resultPacket.first
                    val dataToSend: ByteArray = resultPacket.second
                    Log.d("Packet", "Data: ${packetViewModel.parsingPacket(dataToSend)}")

                    if (isSuccess) {
                        networkManager.sendPacketToServer(dataToSend, packetViewModel, requireContext())
                    } else {
                        Toast.makeText(requireContext(), "패킷 생성 실패", Toast.LENGTH_SHORT).show()
                    }

                    val navController = findNavController()
                    navController.popBackStack(R.id.navigation_home, false)
                }

                deleteButton.setOnClickListener {
                    val context = itemView.context
                    val sharedPreferences = requireContext().getSharedPreferences(PROFILE_PREFS_KEY, Context.MODE_PRIVATE)
                    val selectedProfileName = sharedPreferences.getString("selected_profile", null)
                    if (selectedProfileName != null && selectedProfileName == profile.name) {
                        Toast.makeText(context, "선택된 프로필은 삭제할 수 없습니다.", Toast.LENGTH_SHORT).show()
                    } else {
                        deleteProfile(context, profile.name)
                        updateProfileList()
                        Toast.makeText(context, "${profile.name} 프로필이 삭제되었습니다.", Toast.LENGTH_SHORT)
                            .show()
                    }
                }
            }
        }
    }
}
