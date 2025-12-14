<h1>Tech Support Contact Tool</h1>

<p>
  Internal desktop tool for submitting tech support requests via email.<br />
  Provides a fast, consistent way for employees to contact the tech support team without manually composing emails.
</p>

<hr />

<h2>Overview</h2>
<p>
  The Tech Support Contact Tool is a lightweight <strong>Windows desktop application</strong> built with Python and Tkinter.
</p>
<p>
  Users enter a <strong>title</strong> and <strong>description</strong> of their issue, and the tool sends it as an email through the user’s
  existing Outlook session to a predefined list of support recipients.
</p>
<p>
  Status: <strong>actively used internally</strong>.
</p>

<hr />

<h2>Features</h2>
<ul>
  <li>Simple desktop GUI</li>
  <li>Sends support requests via Outlook using the currently logged-in account</li>
  <li><strong>Title</strong> → email subject</li>
  <li><strong>Description</strong> → email body</li>
  <li>Success / failure feedback after each send</li>
  <li>
    Admin panel (password-protected):
    <ul>
      <li>Manage support email recipients</li>
      <li>Manage predefined support topics (optional dropdown)</li>
      <li>Change admin password</li>
    </ul>
  </li>
  <li>Recipient and topic data stored on shared company storage</li>
  <li>Registry-based fallback if shared storage is temporarily unavailable</li>
</ul>

<hr />

<h2>Requirements</h2>
<ul>
  <li><strong>Windows</strong></li>
  <li><strong>Outlook Desktop</strong> installed and logged in</li>
  <li>Network access to company shared storage</li>
</ul>

<hr />

<h2>Running the App</h2>
<p>
This repository contains the application source code.
End users receive a pre-built <strong>Windows executable</strong> distributed separately.
</p>
<p>No Python installation is required for end users.</p>

<hr />


<h2>Usage</h2>
<ol>
  <li>
    Enter a <strong>title</strong> describing the issue
    <ul>
      <li>(Optional) select a predefined support topic to auto-fill the title</li>
    </ul>
  </li>
  <li>Enter a <strong>description</strong> of the problem</li>
  <li>Click <strong>Send</strong></li>
  <li>A confirmation message will indicate success or failure</li>
</ol>

<hr />

<h2>Admin Access</h2>
<p>The admin panel is built into the same application and is protected by a password.</p>
<p>Admins can:</p>
<ul>
  <li>Edit the list of email recipients</li>
  <li>Edit predefined support topics</li>
  <li>Change the admin password</li>
</ul>

<hr />

<h2>Notes &amp; Limitations</h2>
<ul>
  <li>Relies on the local Outlook installation for sending emails</li>
  <li>Does not manage or store user credentials</li>
  <li>No local activity logging beyond email delivery</li>
  <li>Designed for internal use only</li>
</ul>
