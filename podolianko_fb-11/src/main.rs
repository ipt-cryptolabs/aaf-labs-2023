use podolianko_fb_11::cli;
use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    let cli = cli::CLI::new();
    cli.start_repl()?;

    Ok(())
}
