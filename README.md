# Advance Cheque Tracking

ERPNext (version-16) module that tracks advance cheques received against Sales Orders and reminds the
Sales Person and the Accounts person to collect the original cheque once the advance is settled.

## What it does

- Records each cheque against a submitted Sales Order (`Advance Cheque`).
- Moves the cheque to **Return Pending** when the Sales Order is fully billed or its advance is fully
  used (Sales Invoice submit), and back to **Issued** if that invoice is cancelled.
- Alerts both people with a desk pop-up, a bell notification, an email, a reminder at login and a daily digest.
- Stops all reminders once the cheque is marked **Returned** with its actual return date.
- One report, Advance Cheque Report, with a Status filter (Pending, Issued, Return Pending, Returned), plus a workspace.

Full design: [docs/Advance_Cheque_Tracking_Technical_SDD.docx](docs/Advance_Cheque_Tracking_Technical_SDD.docx).

## Install

```bash
bench get-app <repo-url> --branch version-16
bench --site <site> install-app advance_cheque_tracking
bench --site <site> migrate
```

Then open **Advance Cheque Settings** and set the default Accounts Responsible Person. Each Sales Person that
should be notified needs an Employee with a User.

## Demo data and tests

```bash
bench --site <site> execute advance_cheque_tracking.demo.run
bench --site <site> set-config allow_tests true
bench --site <site> run-tests --app advance_cheque_tracking
bench --site <site> set-config allow_tests false
```

The demo creates three test users (password `Demo@12345`). Remove them on a production site.

## License

MIT
