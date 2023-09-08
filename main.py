import customtkinter
import database
import functions
from ttkwidgets.autocomplete import AutocompleteEntry
from tkintermapview import TkinterMapView
from PIL import Image


def get_index_of_value(my_dict, value):
    values_list = list(my_dict.values())
    if value in values_list:
        return values_list.index(value) + 1
    else:
        return None


class App(customtkinter.CTk):
    APP_NAME = "RTEC Rute Chisinau"
    WIDTH = 1000
    HEIGHT = 800

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)
        self.iconbitmap("rtec.ico")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Command-q>", self.on_closing)
        self.bind("<Command-w>", self.on_closing)
        self.createcommand('tk::mac::Quit', self.on_closing)

        # ============ create two CTkFrames ============

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self, width=300, corner_radius=0, fg_color=None)
        self.frame_left.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")

        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_right.grid(row=0, column=0, rowspan=1, pady=0, padx=0, sticky="nsew")

        # ============ frame_left ============

        self.frame_left.grid_rowconfigure(4, weight=1)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Resetează",
                                                fg_color="#202f5b",
                                                hover_color="#1151d3",
                                                command=self.clear_all)
        self.button_1.grid(pady=(20, 20), padx=(20, 20), row=0, column=0)

        # plecare
        self.start_label = customtkinter.CTkLabel(self.frame_left, text="Punctul de plecare:", anchor="w")
        self.start_label.grid(row=1, column=0, padx=(20, 20), pady=(20, 0))
        self.start_entry = AutocompleteEntry(self.frame_left, width=15, font=('Montserrat', 14),
                                             completevalues=list(database.stops.values()))
        self.start_entry.grid(row=1, column=0, padx=(20, 20), pady=(100, 0))

        # destinatie
        self.end_label = customtkinter.CTkLabel(self.frame_left, text="Destinația:", anchor="w")
        self.end_label.grid(row=2, column=0, padx=(20, 20), pady=(20, 0))
        self.end_entry = AutocompleteEntry(self.frame_left, width=15, font=('Montserrat', 14),
                                           completevalues=list(database.stops.values()))
        self.end_entry.grid(row=2, column=0, padx=(20, 20), pady=(120, 0))

        # recomanda ruta

        self.rec_btn = customtkinter.CTkButton(master=self.frame_left,
                                               text="Recomandă rute",
                                               fg_color="#202f5b",
                                               hover_color="#1151d3",
                                               command=self.recommend_route)
        self.rec_btn.grid(pady=(50, 0), padx=(20, 20), row=3, column=0)

        # rezultate

        self.result_frame = customtkinter.CTkFrame(master=self.frame_left,
                                                   fg_color=None,

                                                   )
        self.result_frame.grid(row=4, column=0, padx=20, pady=20, sticky="nsew")

        # minimum bus number
        self.bus_quantity_label = customtkinter.CTkLabel(master=self.result_frame,
                                                         text="Numărul de troleibuze necesare:",
                                                         font=("Montserrat", 13, "bold"))
        self.bus_quantity_label.grid(row=0, column=0, padx=(20, 20), pady=(20, 0))

        self.bus_quantity_entry = customtkinter.CTkLabel(master=self.result_frame,
                                                         text="",
                                                         font=("Montserrat", 13))
        self.bus_quantity_entry.grid(row=0, column=1, padx=(0, 20), pady=(20, 0))

        # route taken

        self.route_taken_label = customtkinter.CTkLabel(master=self.result_frame,
                                                        text="Traseul recomandat:",
                                                        font=("Montserrat", 13, "bold"))
        self.route_taken_label.grid(row=1, column=0, padx=(20, 20), pady=(20, 0))

        self.route_taken_entry = customtkinter.CTkLabel(master=self.result_frame,
                                                        text="",
                                                        font=("Montserrat", 13),
                                                        anchor="se",
                                                        )
        self.route_taken_entry.grid(row=2, column=0, padx=(20, 0), pady=(0, 0))


        # estimated time

        self.time_label = customtkinter.CTkLabel(master=self.result_frame,
                                                 text="Timpul estimat:",
                                                 font=("Montserrat", 13, "bold"))
        self.time_label.grid(row=3, column=0, padx=(20, 20), pady=(20, 0))

        self.time_entry = customtkinter.CTkLabel(master=self.result_frame,
                                                 text="",
                                                 font=("Montserrat", 13),
                                                 anchor="w"
                                                 )
        self.time_entry.grid(row=3, column=1, padx=(0, 20), pady=(20, 0))



        self.appearance_mode_label = customtkinter.CTkLabel(self.frame_left, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=(20, 20), pady=(20, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.frame_left,
                                                                       fg_color="#202f5b",
                                                                       button_color="#202f5b",
                                                                       button_hover_color="#1151d3",
                                                                       values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=(20, 20), pady=(10, 20))
        # ============ frame_right ============

        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(1, weight=0)
        self.frame_right.grid_columnconfigure(2, weight=1)

        self.map_widget = TkinterMapView(self.frame_right, corner_radius=0)
        self.map_widget.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))

        # program title
        self.program_title = customtkinter.CTkLabel(master=self.frame_right,
                                                    text="Sistem de recomandare a traseelor de troleibuze\n\nGherciu Pavel IA-201",
                                                    font=("Montserrat", 18, "bold"), height=98, width=300,
                                                    wraplength=300)
        self.program_title.grid(row=0, column=0, sticky="we", padx=(12, 0), pady=12)


        # rtec logo

        self.entry = customtkinter.CTkImage(light_image=Image.open("logo.png"), size=(338, 98))
        self.labelnew = customtkinter.CTkLabel(master=self.frame_right, image=self.entry, text="")
        self.labelnew.grid(row=0, column=1, sticky="we", padx=(12, 0), pady=12)

        # Set default values
        self.map_widget.set_address("Chisinau, Moldova")
        self.map_widget.set_zoom(12)
        self.map_widget.set_polygon([(47.0716823, 28.8596493),
                                    (47.0691523, 28.8968998),
                                    (47.0094355, 28.8972002),
                                    (46.9946365, 28.9080149),
                                    (46.9880208, 28.9085846),
                                    (46.9735502, 28.8961002),
                                    (46.9688109, 28.8830077),
                                    (46.9706137, 28.8527524),
                                    (46.9798696, 28.8428828),
                                    (46.9910867, 28.8205923),
                                    (46.9981083, 28.8074602),
                                    (47.0267171, 28.7720215),
                                    (47.0411074, 28.7514222),
                                    (47.0509916, 28.7634593),
                                    (47.0539682, 28.7778777),
                                    (47.0590555, 28.7873062),
                                    (47.0667717, 28.8331639),
                                    (47.0713901, 28.8575498),
                                    ],
                                    outline_color="#202f5b",
                                    border_width=8)
        self.appearance_mode_optionemenu.set("Light")

    def clear_all(self):
        self.map_widget.delete_all_path()
        self.map_widget.delete_all_marker()
        self.bus_quantity_entry.configure(text="")
        self.route_taken_entry.configure(text="")
        self.time_entry.configure(text="")
        self.start_entry.delete(0, "end")
        self.end_entry.delete(0, "end")

    def clear(self):
        self.map_widget.delete_all_path()
        self.map_widget.delete_all_marker()

    def change_appearance_mode(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def paint_path(self, list, input_color):
        self.map_widget.set_path(list, color = input_color, name = "test")

    def paint_markers(self, start, end):
        start_coord = functions.get_specific_coord(database.stops_coord, start)
        end_coord = functions.get_specific_coord(database.stops_coord, end)
        self.map_widget.set_marker(start_coord[0], start_coord[1], text="Pornire")
        self.map_widget.set_marker(end_coord[0], end_coord[1], text="Destinație")

    def recommend_route(self):
        self.clear()
        source = get_index_of_value(database.stops, self.start_entry.get())
        target = (get_index_of_value(database.stops, self.end_entry.get()))
        print(source)
        print(target)
        self.paint_markers(source, target)
        num_buses, route = functions.numBusesToDestination(database.routes, source, target, database.stops_map)
        if num_buses == -1:
            self.route_taken_entry.configure(text="Nu este posibil de ajuns la destinație")
        else:
            self.bus_quantity_entry.configure(text=num_buses)
            for i, (bus_number, stop) in enumerate(route):
                bus_nr = functions.bus_check(bus_number)
                if i == 0:
                    self.route_taken_entry.configure(text=f"Începeți la stația {functions.stops_value_list[stop - 1]}")
                elif i == len(route) - 1:
                    self.route_taken_entry.configure(text=self.route_taken_entry.cget(
                        "text") + f"\nLuați troleibuzul nr.{bus_nr} până la stația {functions.stops_value_list[stop - 1]}")
                    self.route_taken_entry.configure(text=self.route_taken_entry.cget(
                        "text") + f"\nAjungeți la stația {functions.stops_value_list[stop - 1]}")
                else:
                    self.route_taken_entry.configure(text=self.route_taken_entry.cget(
                        "text") + f"\nLuați troleibuzul nr.{bus_nr} până la stația {functions.stops_value_list[stop - 1]}")

        time = 0
        for i in range(len(route) - 1):
            a, b = route[i]
            c, d = route[i + 1]
            stops_list = functions.get_stops(b, d, database.routes[c])
            path_color = functions.randomcolor()
            print(stops_list)
            self.paint_path(functions.get_coords(stops_list), path_color)
            time += functions.travel_time(stops_list)
        print("This is the total time passed:")
        self.time_entry.configure(text=str(time) + " minute")
        print(time)

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
