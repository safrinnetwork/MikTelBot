def get_menu():
    return (
        "Selamat datang di Bot MikroTik!\n\n"
        "Perintah yang tersedia:\n"
        "/interface_list - Menampilkan daftar interface MikroTik\n"
        "/interface_disable <nama_interface> - Disable interface\n"
        "/interface_enable <nama_interface> - Enable interface\n"
        "/interface_status <nama_interface> - Menampilkan status tx dan rx interface\n"
        "/interface_c_name <nama_interface> - Mengganti nama interface\n"
        "/hotspot_user - Menampilkan total user hotspot, total user hotspot aktif, dan total host pada hotspot\n"
        "/hotspot_f_user <nama> - Mencari nama user hotspot\n"
        "/hotspot_detail_user <nama> - Menampilkan detail user hotspot\n"
        "/hotspot_d_user <nama> - Menghapus user hotspot\n"
        "/hotspot_d_active <nama> - Menghapus user aktif hotspot\n"
        "/hotspot_profile_list - Menampilkan daftar profile hotspot\n"
        "/hotspot_ip_binding - Menampilkan daftar IP binding hotspot\n"
    )
