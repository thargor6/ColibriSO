package com.overwhale.colibri_so.frontend.dto;

import lombok.Data;
import org.hibernate.annotations.Type;

import javax.annotation.Nullable;
import java.util.UUID;

@Data
public class SnippetProjectDto {
  @Nullable
  private UUID snippetId;

  @Nullable
  private UUID projectId;
}
