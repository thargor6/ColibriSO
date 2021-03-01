package com.overwhale.colibri_so.frontend.dto;

import lombok.Data;

import javax.annotation.Nullable;
import java.util.UUID;

@Data
public class SnippetIntentDto {
  @Nullable private UUID snippetId;

  @Nullable private UUID intentId;
}
