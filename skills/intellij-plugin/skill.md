# IntelliJ Plugin Development

Expert skill for building IntelliJ IDEA / Android Studio plugins using the IntelliJ Platform SDK, Kotlin, and Gradle Plugin 2.x.

TRIGGER when: user asks to create, modify, or debug an IntelliJ plugin, JetBrains plugin, or Android Studio plugin. Also triggers on mentions of plugin.xml, ToolWindowFactory, AnAction, or IntelliJ Platform SDK.

## Build Setup (IntelliJ Platform Gradle Plugin 2.x)

### build.gradle.kts
```kotlin
plugins {
    id("org.jetbrains.intellij.platform") version "2.6.0"
    id("org.jetbrains.kotlin.jvm") version "2.1.20"
}

repositories {
    mavenCentral()
    intellijPlatform {
        defaultRepositories()
    }
}

dependencies {
    intellijPlatform {
        // Pick ONE target IDE:
        intellijIdeaCommunity("2025.2")  // or:
        // intellijIdeaUltimate("2025.2")
        // androidStudio("2025.2.1.3")

        // Bundled plugins your plugin depends on:
        // bundledPlugin("org.jetbrains.android")
        // bundledPlugin("com.intellij.java")

        pluginVerifier()
        zipSigner()
        instrumentationTools()
    }
}

intellijPlatform {
    pluginConfiguration {
        id = "com.example.myplugin"
        name = "My Plugin"
        version = project.version.toString()
        ideaVersion {
            sinceBuild = "252"
        }
    }
}

kotlin {
    jvmToolchain(21)
}
```

### gradle.properties
```properties
org.gradle.jvm.args=-Xmx2g
kotlin.stdlib.default.dependency=false
```

### Shadow JAR for dependency conflicts
If bundling libraries that conflict with IDE classpath (e.g., protobuf, Gson):
```kotlin
plugins {
    id("com.gradleup.shadow") version "9.0.0-beta12"
}
tasks {
    shadowJar {
        relocate("com.google.protobuf", "com.example.shadow.protobuf")
        archiveClassifier.set("")
    }
    named("prepareSandbox") {
        dependsOn("shadowJar")
    }
}
```

## plugin.xml

```xml
<idea-plugin>
    <id>com.example.myplugin</id>
    <name>My Plugin</name>
    <vendor>MyCompany</vendor>
    <description><![CDATA[Plugin description here.]]></description>

    <depends>com.intellij.modules.platform</depends>
    <!-- Add more depends as needed -->

    <extensions defaultExtensionNs="com.intellij">
        <toolWindow id="My Tool"
                    factoryClass="com.example.MyToolWindowFactory"
                    anchor="bottom"
                    icon="/icons/toolwindow.svg"/>

        <applicationConfigurable
            parentId="tools"
            instance="com.example.MyConfigurable"
            id="com.example.settings"
            displayName="My Plugin"/>

        <applicationService
            serviceImplementation="com.example.MySettings"/>
    </extensions>
</idea-plugin>
```

## Service Registration

### Modern approach: @Service annotation (preferred for 252+)
```kotlin
// Application-level (singleton)
@Service
class MyAppService {
    companion object {
        fun getInstance(): MyAppService =
            ApplicationManager.getApplication().getService(MyAppService::class.java)
    }
}

// Project-level (one per project)
@Service(Service.Level.PROJECT)
class MyProjectService(private val project: Project) {
    companion object {
        fun getInstance(project: Project): MyProjectService =
            project.getService(MyProjectService::class.java)
    }
}
```

No plugin.xml entry needed for @Service classes. Use plugin.xml `<applicationService>` only for `PersistentStateComponent`.

## Tool Window Factory

```kotlin
class MyToolWindowFactory : ToolWindowFactory, DumbAware {
    override fun createToolWindowContent(project: Project, toolWindow: ToolWindow) {
        val panel = MyPanel(project)
        val content = toolWindow.contentManager.factory.createContent(panel, "", false)
        toolWindow.contentManager.addContent(content)
        Disposer.register(toolWindow.disposable, panel)
    }
}
```

Always implement `DumbAware` unless you need indexing. Always register panels as `Disposable`.

## UI Kit — MANDATORY Components

### NEVER use raw Swing defaults. Always use IntelliJ wrappers:

| Instead of | Use |
|---|---|
| `JTree` + `DefaultTreeCellRenderer` | `Tree` + `ColoredTreeCellRenderer` |
| `JTable` | `JBTable` |
| `JList` | `JBList` |
| `JScrollPane` | `JBScrollPane` |
| `JLabel` | `JBLabel` |
| `JSplitPane` | `JBSplitter` |
| `JButton` with text | `ActionToolbar` with `AnAction` |

### ColoredTreeCellRenderer (theme-aware tree rendering)
```kotlin
class MyTreeRenderer : ColoredTreeCellRenderer() {
    override fun customizeCellRenderer(
        tree: JTree, value: Any?, selected: Boolean, expanded: Boolean,
        leaf: Boolean, row: Int, hasFocus: Boolean
    ) {
        val node = value as? DefaultMutableTreeNode ?: return
        when (val obj = node.userObject) {
            is MyCategory -> {
                append(obj.name, SimpleTextAttributes.REGULAR_BOLD_ATTRIBUTES)
                icon = AllIcons.Nodes.Folder
            }
            is MyItem -> {
                append(obj.name, SimpleTextAttributes.REGULAR_ATTRIBUTES)
                icon = AllIcons.FileTypes.Any_type
            }
        }
    }
}
```

`SimpleTextAttributes` constants:
- `REGULAR_ATTRIBUTES` — normal text
- `REGULAR_BOLD_ATTRIBUTES` — bold headers
- `GRAYED_ATTRIBUTES` — disabled/secondary text
- `ERROR_ATTRIBUTES` — error text

### ActionToolbar (instead of raw JButtons)
```kotlin
val actionGroup = DefaultActionGroup().apply {
    add(object : AnAction("Refresh", "Refresh data", AllIcons.Actions.Refresh) {
        override fun actionPerformed(e: AnActionEvent) { /* ... */ }
        override fun update(e: AnActionEvent) {
            e.presentation.isEnabled = /* condition */
        }
        override fun getActionUpdateThread() = ActionUpdateThread.EDT
    })
    addSeparator()
}

val toolbar = ActionManager.getInstance()
    .createActionToolbar("MyPlugin.Toolbar", actionGroup, true) // true=horizontal
toolbar.targetComponent = this
add(toolbar.component, BorderLayout.NORTH)
```

Always override `getActionUpdateThread()` returning `ActionUpdateThread.EDT`.

### Common AllIcons
```
AllIcons.Actions.Refresh        // Refresh
AllIcons.Actions.Download       // Download/save
AllIcons.Actions.GC             // Delete/trash
AllIcons.Actions.Execute        // Run
AllIcons.Actions.Pause          // Pause/inactive
AllIcons.Actions.MenuSaveall    // Save
AllIcons.General.Add            // Add/create
AllIcons.General.Remove         // Remove
AllIcons.General.Information    // Info
AllIcons.General.ChevronDown    // Dropdown arrow
AllIcons.Nodes.Package          // Package
AllIcons.Nodes.Folder           // Folder
AllIcons.Nodes.DataSchema       // Database/schema
AllIcons.FileTypes.Any_type     // Generic file
```

### Empty State with CardLayout
```kotlin
private val cardLayout = CardLayout()
private val contentPanel = JPanel(cardLayout)

// In init:
contentPanel.add(emptyStatePanel, "empty")
contentPanel.add(mainContent, "content")
cardLayout.show(contentPanel, "empty")

// When data available:
cardLayout.show(contentPanel, "content")
```

### Loading Indicator
```kotlin
icon = AnimatedIcon.Default()  // Spinner in tree nodes
```

## Threading Model

### Rule: Heavy work on pooled thread, UI updates on EDT

```kotlin
ApplicationManager.getApplication().executeOnPooledThread {
    val data = heavyOperation()  // Background
    SwingUtilities.invokeLater {
        if (gen != generation) return@invokeLater  // Discard stale
        updateUI(data)  // EDT
    }
}
```

### Generation counter — prevents stale async results
```kotlin
@Volatile
private var generation = 0L

// When user changes selection:
generation++

// In async callback:
val gen = generation
ApplicationManager.getApplication().executeOnPooledThread {
    val result = fetchData()
    SwingUtilities.invokeLater {
        if (gen != generation) return@invokeLater  // State changed, discard
        applyResult(result)
    }
}
```

### ScheduledExecutorService for polling
```kotlin
private val executor = Executors.newSingleThreadScheduledExecutor { r ->
    Thread(r, "MyPlugin-Monitor").apply { isDaemon = true }
}

executor.scheduleWithFixedDelay({ /* poll */ }, 0, 3, TimeUnit.SECONDS)

// In dispose():
executor.shutdownNow()
```

## Tree View with Lazy Loading

```kotlin
// Add placeholder so node appears expandable
val node = DefaultMutableTreeNode(MyData("name"))
node.add(DefaultMutableTreeNode(LoadingMarker))  // Placeholder child

// Lazy load on expand
tree.addTreeWillExpandListener(object : TreeWillExpandListener {
    override fun treeWillExpand(event: TreeExpansionEvent) {
        val node = event.path.lastPathComponent as? DefaultMutableTreeNode ?: return
        if (/* not loaded yet */) {
            node.removeAllChildren()
            node.add(DefaultMutableTreeNode(LoadingMarker))
            treeModel.reload(node)
            loadDataAsync(node)  // Fetch on background thread
        }
    }
    override fun treeWillCollapse(event: TreeExpansionEvent) {}
})

// Incremental node insertion (streaming)
treeModel.insertNodeInto(newNode, parentNode, parentNode.childCount)
```

### Preserve state during tree updates
```kotlin
// Before reload: capture expanded paths
val expanded = getExpandedPackages()
val existingNodes = collectExistingNodes()

// After rebuild: reuse nodes, restore expanded state
for (pkg in expanded) {
    findNode(pkg)?.let { tree.expandPath(TreePath(it.path)) }
}
```

## Settings & Persistence

```kotlin
@State(name = "MySettings", storages = [Storage("MySettings.xml")])
class MySettings : PersistentStateComponent<MySettings.State> {
    data class State(var myValue: Int = 100)
    private var state = State()
    override fun getState(): State = state
    override fun loadState(state: State) { this.state = state }
}
```

Settings UI with Kotlin DSL:
```kotlin
class MyConfigurable : Configurable {
    override fun createComponent(): JComponent = panel {
        group("Section") {
            row("Label:") {
                spinner(1..1000, 10).bindIntValue(::localValue)
            }
        }
    }
    override fun isModified(): Boolean = /* compare local vs saved */
    override fun apply() { /* save */ }
}
```

## Credential & Secret Storage

**`PersistentStateComponent` stores as PLAIN TEXT XML** in `~/.config/JetBrains/<IDE>/options/`. Any API key stored there is readable by every process on the machine. Never store secrets in state components.

### PasswordSafe — the ONLY correct way to store credentials

`PasswordSafe` delegates to the OS keychain (macOS Keychain, Windows Credential Manager, KWallet/GNOME Keyring):

```kotlin
import com.intellij.credentialStore.CredentialAttributes
import com.intellij.credentialStore.Credentials
import com.intellij.credentialStore.generateServiceName
import com.intellij.ide.passwordSafe.PasswordSafe

object MyCredentialStore {
    private val attributes = CredentialAttributes(
        generateServiceName("MyPlugin", "apiKey")
    )

    fun getToken(): String? =
        PasswordSafe.instance.getPassword(attributes)

    fun setToken(token: String) =
        PasswordSafe.instance.setPassword(attributes, token)

    fun getCredentials(): Credentials? =
        PasswordSafe.instance.get(attributes)

    fun setCredentials(user: String, password: String) =
        PasswordSafe.instance.set(attributes, Credentials(user, password))
}
```

### Environment variable fallback (CI / headless)

```kotlin
fun resolveToken(): String? =
    System.getenv("MY_PLUGIN_API_KEY") ?: MyCredentialStore.getToken()
```

### Settings UI with password field

```kotlin
class MyConfigurable : Configurable {
    private var tokenField = JBPasswordField()

    override fun createComponent(): JComponent = panel {
        group("Authentication") {
            row("API Token:") { cell(tokenField) }
        }
    }
    override fun isModified(): Boolean =
        String(tokenField.password) != (MyCredentialStore.getToken() ?: "")
    override fun apply() {
        MyCredentialStore.setToken(String(tokenField.password))
    }
    override fun reset() {
        tokenField.text = MyCredentialStore.getToken() ?: ""
    }
}
```

### NEVER do any of these:
- Hardcode keys in source code
- Store secrets in `PersistentStateComponent` (plain text XML)
- Log tokens at any level, including DEBUG
- Include credentials in exception messages
- Commit `.env` or `local.properties` containing secrets

## Security Hardening

### Shell command injection

Never build shell commands via string concatenation. Use `ProcessBuilder` with an explicit argument list:

```kotlin
// BAD — injectable
Runtime.getRuntime().exec("adb shell run-as $pkg cat $path")

// GOOD — each argument is a separate element
ProcessBuilder("adb", "shell", "run-as", pkg, "cat", path)
    .redirectErrorStream(true)
    .start()
```

### Input validation

Allowlist characters for user-provided strings passed to shell or file system:

```kotlin
private val SAFE_PATH = Regex("^[a-zA-Z0-9._/-]+$")
private val SAFE_PACKAGE = Regex("^[a-zA-Z0-9._]+$")

fun validatePath(input: String): String {
    require(SAFE_PATH.matches(input)) { "Invalid path: $input" }
    return input
}
```

### File path traversal prevention

```kotlin
fun safePath(base: File, userInput: String): File {
    val resolved = File(base, userInput).canonicalFile
    require(resolved.path.startsWith(base.canonicalPath)) {
        "Path escapes base directory"
    }
    return resolved
}
```

### Network security

- Always use `HttpConfigurable.getInstance()` for proxy-aware HTTP
- Enforce TLS — never disable certificate verification, even during development
- Never use `ObjectInputStream` on untrusted data — prefer JSON/protobuf with schema validation

## Logging & Error Handling

### Logger — never println

```kotlin
private val log = Logger.getInstance(MyService::class.java)

log.error("Unexpected failure in sync")   // Shown in IDE error reporter
log.warn("Device disconnected mid-read")  // Recoverable issue
log.info("Plugin initialized")            // Lifecycle events
log.debug("Parsed ${entries.size} items")  // Off by default, zero cost when disabled
```

Never use `println`, `System.out`, or `System.err`. The IDE aggregates `Logger` output in `idea.log` (Help > Diagnostic Tools > Browse Logs).

### Notification API for user-facing messages

Register the notification group in `plugin.xml`:
```xml
<extensions defaultExtensionNs="com.intellij">
    <notificationGroup id="MyPlugin.Notifications"
                        displayType="BALLOON"/>
</extensions>
```

Then use it in code:
```kotlin
NotificationGroupManager.getInstance()
    .getNotificationGroup("MyPlugin.Notifications")
    .createNotification("Sync completed", NotificationType.INFORMATION)
    .notify(project)
```

### Anti-patterns
- Never show raw stack traces to users — use `Notification` with a human message
- Never swallow exceptions silently — at minimum `log.warn()`
- Never use `log.error()` for expected conditions like "device not connected"

## Testing Strategy

### Plain JUnit for logic-only classes

Use JUnit directly for classes with no IDE dependency (parsers, utilities):
```kotlin
class MyParserTest {
    @Test
    fun `parse valid input`() {
        val result = MyParser.parse(testBytes)
        assertEquals(3, result.size)
    }
}
```

### BasePlatformTestCase for IDE integration

```kotlin
class MyServiceTest : BasePlatformTestCase() {
    fun testServiceReturnsData() {
        val service = project.getService(MyProjectService::class.java)
        val result = service.fetchData()
        assertNotNull(result)
    }
}
```

Note: `BasePlatformTestCase` uses JUnit 3 conventions — test methods must start with `test`, no annotations.

### Mock services

Replace real services with test doubles using `ServiceContainerUtil`:
```kotlin
import com.intellij.testFramework.ServiceContainerUtil

fun setUp() {
    super.setUp()
    ServiceContainerUtil.replaceService(
        ApplicationManager.getApplication(),
        MyAppService::class.java,
        FakeMyAppService(),
        testRootDisposable
    )
}
```

### Test fixtures

Place test data in `src/test/resources/` and load via:
```kotlin
val bytes = javaClass.getResourceAsStream("/fixtures/sample.pb")!!.readBytes()
```

### UI testing

Test logic separately from UI. For integration tests that need EDT:
```kotlin
import com.intellij.testFramework.runInEdtAndWait

fun testUIUpdate() {
    runInEdtAndWait {
        panel.loadData(testEntries)
        assertEquals(3, table.rowCount)
    }
}
```

Full UI testing (clicking buttons, expanding trees) is fragile and usually not worth the maintenance cost.

## Icons

### File structure
```
src/main/resources/icons/
    toolwindow.svg        # 13x13, #6E6E6E fill (light theme)
    toolwindow_dark.svg   # 13x13, #AFB1B3 fill (dark theme, auto-detected by _dark suffix)
    pluginIcon.svg        # 40x40, full color (marketplace listing)
```

### Icon loader
```kotlin
object MyIcons {
    @JvmField
    val ToolWindow: Icon = IconLoader.getIcon("/icons/toolwindow.svg", MyIcons::class.java)
}
```

IntelliJ auto-selects `_dark.svg` variant based on active theme.

## Disposable Lifecycle

Every component that creates threads, executors, sockets, or listeners MUST implement `Disposable`:
```kotlin
class MyComponent : Disposable {
    private val executor = Executors.newSingleThreadScheduledExecutor(...)

    override fun dispose() {
        executor.shutdownNow()
        // Close sockets, cancel tasks, clear state
    }
}
```

Register with parent: `Disposer.register(toolWindow.disposable, myComponent)`

## Plugin Signing & Publishing

### Signing configuration

Add to `build.gradle.kts`. Credentials come from environment variables — never commit them:

```kotlin
intellijPlatform {
    signing {
        certificateChainFile = file("chain.crt")
        privateKeyFile = file("private.pem")
        password = providers.environmentVariable("PRIVATE_KEY_PASSWORD")
    }
    publishing {
        token = providers.environmentVariable("PUBLISH_TOKEN")
    }
}
```

Generate a key pair via the [JetBrains Marketplace](https://plugins.jetbrains.com/author/me/tokens). Store `chain.crt`, `private.pem`, and the token outside version control.

### Plugin icons for Marketplace

Place in `META-INF/` (not `icons/`). These are distinct from toolwindow icons:

```
src/main/resources/META-INF/
    pluginIcon.svg       # 40x40, full color — used in Marketplace listing and IDE plugin manager
    pluginIcon_dark.svg  # 40x40, dark variant — auto-selected by IDE
```

### Version compatibility

- `sinceBuild = "252"` — minimum IDE build your plugin supports
- Omit `untilBuild` to support all future versions (Gradle plugin does this by default)
- Run `./gradlew runPluginVerifier` to catch binary incompatibilities before release
- Add target IDE versions to verify against:

```kotlin
intellijPlatform {
    pluginVerification {
        ides {
            recommended()
        }
    }
}
```

### Pre-submission checklist

- [ ] `./gradlew runPluginVerifier` passes with no API compatibility errors
- [ ] Plugin description is at least 40 words
- [ ] `<vendor>` has `url` and `email` attributes set
- [ ] Change notes describe user-facing changes (not commit log)
- [ ] Test install from disk on a clean IDE instance
- [ ] No `@ApiStatus.Internal` or deprecated API usage
- [ ] Plugin icon renders correctly in dark and light themes
- [ ] `META-INF/NOTICE` file lists all bundled third-party dependencies with their licenses

### Third-party license notice

If your plugin bundles any third-party libraries (e.g., protobuf, Gson, OkHttp), include a `NOTICE` file in `src/main/resources/META-INF/NOTICE` with:
- Plugin copyright
- Each dependency's name, copyright holder, license type, and full license text

```
src/main/resources/META-INF/
    NOTICE           # Third-party license attributions (bundled in JAR)
```

This is required for BSD, MIT, and Apache-licensed dependencies. GPL dependencies cannot be bundled in proprietary plugins.

## Architecture Patterns

### Service level decision

| Level | Scope | When to use | Example |
|---|---|---|---|
| `@Service` | Application | Global singletons, shared state across projects | Credential store, HTTP client |
| `@Service(Service.Level.PROJECT)` | Project | State tied to a specific project | File monitors, project caches |

Rule of thumb: if the constructor needs a `Project` parameter, it is project-level.

### Message bus — decoupled event communication

Define a topic:
```kotlin
interface DataChangedListener {
    fun onDataChanged(entries: List<DataEntry>)

    companion object {
        val TOPIC = Topic.create("MyPlugin.DataChanged", DataChangedListener::class.java)
    }
}
```

Publish:
```kotlin
project.messageBus.syncPublisher(DataChangedListener.TOPIC).onDataChanged(entries)
```

Subscribe (always pass a `Disposable` to prevent leaks):
```kotlin
project.messageBus.connect(parentDisposable).subscribe(
    DataChangedListener.TOPIC,
    object : DataChangedListener {
        override fun onDataChanged(entries: List<DataEntry>) { /* update UI */ }
    }
)
```

### Coroutines (2024.1+)

For plugins targeting recent IDE versions, coroutines provide structured concurrency:
```kotlin
@Service(Service.Level.PROJECT)
class MyService(private val project: Project, private val scope: CoroutineScope) {
    fun refreshAsync() = scope.launch {
        val data = withContext(Dispatchers.IO) { fetchFromDevice() }
        withContext(Dispatchers.EDT) { updateUI(data) }
    }
}
```

The `executeOnPooledThread` + `SwingUtilities.invokeLater` pattern remains simpler and compatible with all IDE versions.

### Virtual File System (VFS)

Prefer VFS over `java.io.File` when working with IDE-managed files:
```kotlin
val vFile = LocalFileSystem.getInstance().findFileByPath("/path/to/file")
vFile?.let { VfsUtil.loadText(it) }
```

VFS provides change notifications, is thread-safe, and integrates with IDE indexing.

## Performance & Compatibility

### Memory leak prevention

- Use `Disposer.register(parent, child)` to chain disposal — never register a listener without a corresponding disposal
- Message bus connections auto-disconnect when the parent is disposed: `messageBus.connect(parentDisposable)`
- Use `WeakReference` for listeners registered on long-lived objects (application, project)
- Never store `Project` or `Component` references in application-level services

### Lazy initialization

Services are already lazy (instantiated on first `getService()` call). For expensive fields within services:
```kotlin
private val cache by lazy { buildExpensiveCache() }
```

### EDT blocking detection

Enable in development to catch slow operations on the UI thread:
```
-Dide.slow.operations.assertion=true
```
Any operation over ~300ms on EDT triggers a warning. Common offenders: file I/O, network calls, `Process.waitFor()`, large tree rebuilds.

### IDE version compatibility

- Run `./gradlew runPluginVerifier` against target IDE versions before every release
- Never call `@ApiStatus.Internal` APIs — they change without notice between IDE versions
- Avoid `@ApiStatus.Experimental` in production — they may be removed
- For version-specific APIs, use reflection or try/catch:
```kotlin
try {
    // New API available in 2025.2+
    NewApi.doSomething()
} catch (e: NoSuchMethodError) {
    // Fallback for older versions
    OldApi.doSomething()
}
```

## Security Audit Prompt

When asked to audit an IntelliJ plugin for security vulnerabilities, systematically check every source file for the following categories. Report each finding with file path, line number, code snippet, risk description, and severity (Critical/High/Medium/Low).

### 1. XML External Entity (XXE) Injection
Any use of `DocumentBuilderFactory`, `SAXParserFactory`, `XMLInputFactory`, or `TransformerFactory` without disabling external entities. A malicious XML file (config, data, or user-uploaded) can read arbitrary files from the host machine (`~/.ssh/id_rsa`, `~/.env`, `/etc/passwd`).

**What to grep for:** `DocumentBuilderFactory`, `SAXParser`, `XMLInputFactory`, `TransformerFactory`, `.parse(`
**Fix pattern:**
```kotlin
val factory = DocumentBuilderFactory.newInstance().apply {
    setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd", false)
    setFeature("http://xml.org/sax/features/external-general-entities", false)
    setFeature("http://xml.org/sax/features/external-parameter-entities", false)
}
```

### 2. Shell Command Injection
Any place where external input (package names, file paths, user strings, device identifiers) flows into `ProcessBuilder`, `Runtime.exec()`, or especially `sh -c` commands via string interpolation.

**What to grep for:** `ProcessBuilder`, `Runtime.getRuntime().exec`, `"sh"`, `"-c"`, string templates inside command lists
**Red flags:**
- `sh -c "$userInput"` — full shell injection
- `ProcessBuilder("sh", "-c", "command $variable")` — injectable even with ProcessBuilder
- String concatenation in any argument passed to a shell interpreter
**Verify:** Every variable interpolated into a shell command has strict allowlist validation upstream. Trace the data flow from origin to shell invocation.

### 3. Input Validation — Overly Permissive Allowlists
Regex-based validators that permit characters unnecessary for the domain. Wider allowlists = wider attack surface, especially when values end up in shell commands or file paths.

**What to grep for:** `Regex(`, `matches(`, `require(`, validation patterns
**Check:** For each validator, ask: does this allow any character that could be a shell metacharacter (`; | & $ \` ' " ( ) { } < > ! #`) or path traversal (`..`)? If the validated string ends up in a shell command, even inside quotes, the allowlist must exclude the quote character used.
**Rule:** `SAFE_PATH` should be `^[a-zA-Z0-9._/-]+$` — no spaces, semicolons, tildes, percent signs, or other shell-meaningful characters unless explicitly required.

### 4. Credential & Secret Exposure
Secrets stored in `PersistentStateComponent` (plain text XML), logged at any level, hardcoded in source, or committed in `.env`/config files.

**What to grep for:** `PersistentStateComponent`, `password`, `token`, `secret`, `apiKey`, `credential`, `log.debug`, `log.info`, `log.warn`, `log.error` (check what they log), `.env`, `local.properties`
**Check:**
- Are secrets stored via `PasswordSafe` (OS keychain) or in plain XML state files?
- Do log statements include tokens, passwords, command output containing auth data?
- Is `.env` / `local.properties` in `.gitignore`?
- Do exception messages or error notifications expose credentials?

### 5. File Path Traversal
User-controlled paths that aren't validated against directory escape (`../../../etc/passwd`).

**What to grep for:** `File(`, `Paths.get(`, `resolve(`, `filePath`, `fileName`, user-provided strings used in file operations
**Check:** Every path derived from external input must be canonicalized and confirmed to stay within an expected base directory:
```kotlin
val resolved = File(base, userInput).canonicalFile
require(resolved.path.startsWith(base.canonicalPath))
```

### 6. Unsafe Deserialization
`ObjectInputStream` on data from external sources (files from devices, network responses, plugin state). Can lead to arbitrary code execution.

**What to grep for:** `ObjectInputStream`, `readObject()`, `Serializable`
**Fix:** Use JSON, protobuf, or other schema-validated formats instead.

### 7. Network Security
HTTP instead of HTTPS, disabled certificate verification, ignoring proxy settings, sending local data to external services.

**What to grep for:** `http://` (not `https://`), `TrustManager`, `HostnameVerifier`, `SSLContext`, `HttpURLConnection`, `OkHttpClient`, `setHostnameVerifier`
**Check:**
- All URLs use HTTPS
- No custom `TrustManager` that accepts all certificates
- Uses `HttpConfigurable.getInstance()` for proxy-aware connections
- No local file contents, paths, or environment data sent to remote endpoints without user consent

### 8. Temporary File Handling
Temp files with sensitive content that aren't cleaned up, or temp files in world-readable locations.

**What to grep for:** `createTempFile`, `createTempDir`, `File.createTempFile`, `/tmp/`, `System.getProperty("java.io.tmpdir")`
**Check:** Are temp files deleted in a `finally` block or `use {}` scope? Do they contain sensitive data (credentials, user content from devices)?

### 9. Build Configuration Leakage
Signing credentials, publish tokens, or API keys in `build.gradle.kts` that could leak through build logs, CI artifacts, or Gradle cache.

**What to grep for:** `signing`, `publishing`, `password`, `token` in `*.gradle.kts` and `*.properties` files
**Check:** Credentials come from environment variables or secure vaults, not hardcoded strings. Build scripts don't print sensitive values.

### 10. Information Disclosure via Logging
Log statements that include sensitive data: file contents, user data from devices, full command lines with paths/credentials, stack traces with sensitive context.

**What to grep for:** `log.warn`, `log.error`, `log.info`, `log.debug` — inspect what variables are interpolated
**Rule:** Log the *event* and *error type*, not the *data*. E.g., `log.warn("Failed to read file", e)` not `log.warn("Failed to read $filePath: content=$data")`.

### Audit Procedure

1. Glob all `.kt`, `.java`, `.gradle.kts`, `.properties`, and `.xml` source files
2. For each category above, grep for the listed patterns across all files
3. For each match, trace the data flow: where does the input originate, how is it validated, where does it end up?
4. Report findings grouped by severity, with exact file:line references and fix recommendations
5. Also note positive security measures already in place (proper validation, PasswordSafe usage, etc.)

## Pitfall Checklist

- [ ] Use `ColoredTreeCellRenderer`, NOT `DefaultTreeCellRenderer` (broken in dark theme)
- [ ] Use `ActionToolbar` with `AnAction`, NOT raw `JButton` for toolbars
- [ ] Override `getActionUpdateThread()` returning `ActionUpdateThread.EDT` in every `AnAction`
- [ ] Set `toolbar.targetComponent = this` on every `ActionToolbar`
- [ ] Use generation counters for all async operations that update UI
- [ ] Call `executor.shutdownNow()` in every `Disposable.dispose()`
- [ ] Use `exec-out` not `shell` for binary-safe ADB data transfer
- [ ] Batch ADB operations in shell scripts to minimize round-trips
- [ ] Test with real device data, not just assumptions about wire formats
- [ ] Shadow/relocate dependencies that conflict with IDE classpath
- [ ] Provide both `toolwindow.svg` and `toolwindow_dark.svg` for icon theming
- [ ] Implement `DumbAware` on `ToolWindowFactory` unless indexing is required
- [ ] Use `JBUI.scale()` for DPI-aware sizes
- [ ] Never store API keys or tokens in `PersistentStateComponent` — use `PasswordSafe`
- [ ] Never build shell commands via string concatenation — use `ProcessBuilder` argument lists
- [ ] Validate all user-provided file paths against directory traversal (`../`)
- [ ] Use `Logger.getInstance()`, never `println` or `System.out` / `System.err`
- [ ] Never log credentials, tokens, or sensitive user data at any log level
- [ ] Register notification groups in `plugin.xml` before using `NotificationGroupManager`
- [ ] Run `runPluginVerifier` before every Marketplace submission
- [ ] Provide `META-INF/pluginIcon.svg` (40x40) and `pluginIcon_dark.svg` for Marketplace listing
- [ ] Connect message bus subscriptions to a `Disposable` to prevent leaks
- [ ] Use `WeakReference` for listeners on long-lived objects (application, project)
- [ ] Never call `@ApiStatus.Internal` APIs in production plugin code
- [ ] Sign the plugin with `signPlugin` task before publishing to Marketplace
